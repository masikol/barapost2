
import sys
import logging
from functools import reduce
from typing import Sequence, TypeAlias

import src.filesystem as fs
from src.util.prune_seq import prune_seq
from src.args.ProberArgs import ProberArgs
import src.remote_blast.blast_errors as berr
from src.containers.HTSRecord import HTSRecord
from src.containers.SeqRecord import SeqRecord
from src.containers.AlignResult import AlignResult
from src.reader_system.FileReader import FileReader
from src.remote_blast.RemoteBlast import RemoteBlast
from src.seq_db.SeqDbListManager import SeqDbListManager
from src.taxonomy.TaxonomyManager import TaxonomyManager
from src.reader_system.ReaderWrapper import ReaderWrapper
from src.containers.Fastq import Fastq, make_quality_dict
from src.util.BarapostWorkDirManager import BarapostWorkDirManager


# TODO: RELEASE: don't forget to move higher to some config abstraction level
logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)


ActionCode : TypeAlias = str

ACTION_RESUME  : ActionCode = '1'
ACTION_REWRITE : ActionCode = '2'
ACTION_ARCHIVE : ActionCode = '3'
ACTION_EXIT    : ActionCode = '4'


SeqPacket : TypeAlias = Sequence[SeqRecord]
AlignResultDict : TypeAlias = dict[str, Sequence[AlignResult]]


class ProberKernel:

    def __init__(self, args : ProberArgs):
        self.args = args
        self.work_dir_manager = BarapostWorkDirManager(args.output_dirpath)
        self.remote_blast = RemoteBlast(
            blast_algorithm=args.blast_algorithm,
            organisms=args.organisms,
            output_dirpath=args.output_dirpath,
        )
        self.taxonomy_manager = TaxonomyManager(args.output_dirpath)
        self.seq_db_list_manager = SeqDbListManager(args.output_dirpath)
    # end def


    def run(self):
        n_first_skip_dict = self._handle_previous_run()

        self._retrieve_old_run_jobs(n_first_skip_dict)

        input_fpaths_by_type = self._split_input_fpaths_by_type()

        for input_fpaths in input_fpaths_by_type:
            reader_wrapper = ReaderWrapper(
                file_paths=input_fpaths,
                probing_batch_size=self.args.probing_batch_size,
                packet_mode=self.args.packet_mode,
                packet_size=self.args.packet_size,
                max_seq_len=self.args.max_seq_len,
                n_first_skip_dict=n_first_skip_dict
            )

            with reader_wrapper as seq_reader:
                for packet in seq_reader:
                    # TODO: passing seq_reader is ugly.
                    #   Make it a class field?
                    self._classify_packet(packet, seq_reader)
                # end for
            # end with
        # end for
        logging.info('The probing batch has been classified!')
    # end def

    def _handle_previous_run(self) -> dict:

        n_first_skip_dict = self._look_around()

        resume_action = None
        num_records_to_skip = sum(
            n for n in n_first_skip_dict.values()
        )
        if num_records_to_skip > 0:
            resume_action = self._ask_for_resumption()
        # end if

        # _ask_for_resumption ensures that resume_action holds proper value
        if resume_action == ACTION_ARCHIVE:
            self.work_dir_manager.archive_workdir_files()
            n_first_skip_dict = dict() # empty it: start from the beginning
            self.taxonomy_manager = TaxonomyManager(
                self.work_dir_manager.work_dirpath
            )
            self.seq_db_list_manager = SeqDbListManager(
                self.work_dir_manager.work_dirpath
            )
        elif resume_action == ACTION_REWRITE:
            self.work_dir_manager.remove_workdir_files()
            n_first_skip_dict = dict() # empty it: start from the beginning
            self.taxonomy_manager = TaxonomyManager(
                self.work_dir_manager.work_dirpath
            )
            self.seq_db_list_manager = SeqDbListManager(
                self.work_dir_manager.work_dirpath
            )
        elif resume_action == ACTION_EXIT:
            logging.info('Bye!')
            sys.exit(0)
        # end if

        return n_first_skip_dict
    # end def

    def _look_around(self) -> dict:
        n_first_skip_dict = dict()

        for input_fpath in self.args.input_fpaths:
            n_classified_seqs = self.work_dir_manager.count_classification_records(
                input_fpath
            )
            n_first_skip_dict[input_fpath] = 0
            if n_classified_seqs > 0:
                logging.info(
                    'Found that {:,} sequences from file `{}` have been already classified'.format(
                        n_classified_seqs,
                        input_fpath
                    )
                )
                # Argument parsing ensures abspath here
                n_first_skip_dict[input_fpath] = n_classified_seqs
            # end if
        # end for

        return n_first_skip_dict
    # end def

    def _ask_for_resumption(self) -> ActionCode:
        # Function asks a user if he/she wants to resume the previous run.
        # Returns True if the decision is to resume, else False

        resume = None
        allowed_values = (
            ACTION_RESUME,
            ACTION_REWRITE,
            ACTION_ARCHIVE,
            ACTION_EXIT,
        )

        prompt = '''
    Would you like to resume the previous run?
       {} -- Yes, resume!
       {} -- Remove the old results and start from the beginning.
       {} -- Archive the old results and start from the beginning.
       {} -- Exit now.

    Enter a number ({}):>> '''.format(
            ACTION_RESUME, ACTION_REWRITE, ACTION_ARCHIVE, ACTION_EXIT,
            ' or '.join(allowed_values)
        )

        while resume is None:
            resume = input(prompt)
            resume = resume.strip()
            # Validate input
            # Check if input number is '1' or '2'
            if not resume in allowed_values:
                logging.warning(
                    'Invalid value entered: `{}`!\a'.format(resume) + '~'*20
                )
                resume = None
            else:
                if resume == ACTION_RESUME:
                    action_log = 'resume the previous run'
                elif resume == ACTION_REWRITE:
                    action_log = 'remove the old results and start from the beginning'
                elif resume == ACTION_ARCHIVE:
                    action_log = 'archive the old results and start from the beginning'
                else:
                    action_log = 'exit now'
                # end if
                # end if
                logging.info('You have chosen to {}.'.format(action_log))
            # end if

        return resume
    # end def

    def _retrieve_old_run_jobs(self, n_first_skip_dict : dict[str, int]):
        for input_fpath in self.args.input_fpaths:
            tmp_data = self.work_dir_manager.load_tmp_remote_blast_file(
                input_fpath
            )
            if tmp_data is None:
                continue
            # end if
            logging.info('Found saved data for file `{}`'.format(input_fpath))
            try:
                align_results = self.remote_blast.retrieve_results(
                    request_id=tmp_data['request_id'],
                    wait_time=0
                )
                self.work_dir_manager.rm_tmp_remote_blast_file(
                    input_fpath
                )
                self._save_align_results_old_job(
                    align_results,
                    tmp_data['fpath'],
                    tmp_data['quality_dict'],
                    n_first_skip_dict
                )
            except berr.BlastError as err:
                if err.code == berr.ACTION_NO_HITS:
                    saved_input_fpath = tmp_data['fpath']
                    # Update n_first_skip_dict so that
                    #   retrieved seqs would not be processed repeatedly
                    if not saved_input_fpath in n_first_skip_dict:
                        n_first_skip_dict[saved_input_fpath] = 0
                    # end if
                    n_first_skip_dict[input_fpath] += tmp_data['packet_size']
                elif err.code == berr.ACTION_RESEND:
                    pass # this old packet will be processed as usual
                elif err.code == berr.ACTION_SPLIT_AND_RESEND:
                    pass # this old packet will be processed as usual
                elif err.code == berr.ACTION_PANIC:
                    sys.exit(1)
                # end if
            # end try
        # end for
    # end def


    def _split_input_fpaths_by_type(self) -> Sequence[Sequence[str]]:
        fasta_fpaths = tuple(
            filter(fs.is_fasta, self.args.input_fpaths)
        )
        fastq_fpaths = tuple(
            filter(fs.is_fastq, self.args.input_fpaths)
        )
        output_list = list()
        if len(fasta_fpaths) != 0:
            output_list.append(fasta_fpaths)
        # end if
        if len(fastq_fpaths) != 0:
            output_list.append(fastq_fpaths)
        # end if
        return output_list
    # end def


    def _classify_packet(self,
                         packet : SeqPacket,
                         seq_reader : FileReader):
        logging.info(
            'Submitting {:,} sequences ({:,} bp totally) to BLAST server'.format(
                len(packet),
                sum(
                    (len(sr.get_seq()) for sr in packet)
                )
            )
        )
        try:
            request_id, wait_time = self.remote_blast.submit_remote_blast(
                packet
            )
            self.work_dir_manager.write_tmp_remote_blast_file(
                request_id,
                seq_reader.get_curr_infpath(),
                packet
            )
            align_results = self.remote_blast.retrieve_results(
                request_id=request_id,
                wait_time=wait_time
            )
        except berr.BlastError as err:
            if err.code == berr.ACTION_NO_HITS:
                align_results = self._make_empty_align_results(packet)
                curr_input_fpath = seq_reader.get_curr_infpath()
                self._save_align_results_current_job(
                    align_results,
                    curr_input_fpath,
                    packet
                )
            elif err.code == berr.ACTION_RESEND:
                self._classify_packet(packet, seq_reader)
            elif err.code == berr.ACTION_SPLIT_AND_RESEND:
                smaller_packets = self._split_packet_in_half(packet)
                for smaller_packet in smaller_packets:
                    self._classify_packet(smaller_packet, seq_reader)
                # end for
            elif err.code == berr.ACTION_PANIC:
                logging.critical('Blast panic: exitting immediately!')
                sys.exit(1)
            # end if
        else:
            curr_input_fpath = seq_reader.get_curr_infpath()
            self._save_align_results_current_job(
                align_results,
                curr_input_fpath,
                packet
            )
            self.work_dir_manager.rm_tmp_remote_blast_file(curr_input_fpath)
        # end try
    # end def

    def _save_align_results_current_job(self,
                                        align_results : AlignResultDict,
                                        curr_input_fpath : str,
                                        packet : SeqPacket):
        quality_dict = make_quality_dict(packet)
        align_results = self._add_quality_to_align_results(
            align_results,
            quality_dict
        )
        self._save_align_results(
            align_results,
            curr_input_fpath
        )
    # end def

    def _save_align_results_old_job(self,
                                    align_results : AlignResultDict,
                                    curr_input_fpath : str,
                                    quality_dict : dict[str, float],
                                    n_first_skip_dict : dict[str, int]):
        align_results = self._add_quality_to_align_results(
            align_results,
            quality_dict
        )
        self._save_align_results(
            align_results,
            curr_input_fpath
        )
        n_first_skip_dict[curr_input_fpath] += len(align_results)
    # end def

    def _save_align_results(self,
                            align_results : AlignResultDict,
                            curr_input_fpath : str):
        for query_id, align_result_list in align_results.items():
            for align_result in align_result_list:
                if not align_result.hit_accession is None:
                    self.taxonomy_manager.add_taxonomy(align_result.hit_accession)
                    self.seq_db_list_manager.add_seq_db_record(align_result)
                # end if
                sys.stderr.write(align_result.to_console_summary())
            # end for
        # end if
        self.seq_db_list_manager.rewrite_db()
        self.taxonomy_manager.rewrite_taxonomy_file()
        self._save_classif_results(align_results, curr_input_fpath)
    # end def

    def _add_quality_to_align_results(self,
                                      align_results : AlignResultDict,
                                      quality_dict : dict[str, float]) -> AlignResultDict:
        try:
            for query_id, align_result_list in align_results.items():
                first_result = next(iter(align_result_list))
                seq_quality = quality_dict[query_id]
                tuple( # run map
                    map(
                        lambda ar: ar.add_query_quality(seq_quality),
                        align_result_list
                    )
                )
            # end for
        except KeyError:
            logging.critical(
                'Fatal error: quality not found in quality_dict. ' \
                'Error code: `_add_quality_to_align_results.1`'
            )
            sys.exit(1)
        # end try
        return align_results
    # end def

    def _save_classif_results(self,
                              align_results : AlignResultDict,
                              curr_input_fpath : str):
        classif_fpath = self.work_dir_manager.make_classification_fpath(
            curr_input_fpath
        )
        classif_record_count = self.work_dir_manager.count_classification_records(
            curr_input_fpath
        )
        if classif_record_count < 1:
            self.work_dir_manager.write_classification_header(curr_input_fpath)
        # end if
        with open(classif_fpath, 'at') as output_handle:
            for align_result_list in align_results.values():
                merged_align_result = reduce(
                    AlignResult.merge,
                    align_result_list
                )
                output_handle.write(
                    merged_align_result.to_tsv_row()
                )
            # end for
        # end with
    # end def

    def _make_empty_align_results(self,
                                  packet : SeqPacket) -> AlignResultDict:
        return {
                sr.get_seq_id() : [
                    AlignResult.make_empty_result(
                        sr.get_seq_id(),
                        len(sr.seq)
                    )
                ]
                for sr in packet
        }
    # end def

    def _split_packet_in_half(self,
                              packet : SeqPacket) -> Sequence[SeqPacket]:
        old_packet_len = len(packet)
        if old_packet_len > 1:
            # Split current packet into two (of equal number of sequences) and resubmit them one-by-one
            logging.info(
                'Splitting current packet into two and submitting each of them one-by-one.'
            )

            new_pack_size = self._calculate_half_packet_len(old_packet_len)
            smaller_packets = tuple(
                [packet[: new_pack_size]],
                [packet[new_pack_size: ]],
            )
        elif old_packet_len == 1:
            # Prune the only sequence in packet and resend it
            logging.info('Current packet contains only one sequence.')
            logging.info(
                'Prober will prune this sequence in half and resubmit it.'
            )

            old_seq_record = next(iter(packet))
            new_seq_len = self._calculate_half_seq_len(old_seq_record)
            new_seq_record = prune_seq(old_seq_record, new_seq_len)
            smaller_packets = tuple(
                new_seq_record,
            )
        else:
            logging.warning('Cannot split packet: it is empty')
            # TODO: or raise an exception?
            return tuple()
        # end if
        return smaller_packets
    # end def

    def _calculate_half_packet_len(self, old_packet_len : int) -> int:
        new_packet_size = old_packet_len // 2
        if old_packet_len % 2 != 0:
            new_packet_size += 1
        # end if
        return new_packet_size
    # end def

    def _calculate_half_seq_len(self, seq_record : HTSRecord) -> int:
        old_seq_len = len(seq_record.get_seq())
        new_seq_len = old_seq_len // 2
        if old_seq_len % 2 != 0:
            new_seq_len += 1
        # end if
        return new_seq_len
    # end def
# end class
