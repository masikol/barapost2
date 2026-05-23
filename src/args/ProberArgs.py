
import os
import re
import sys
import glob
import argparse
from typing import Sequence

import src.filesystem as fs
import src.config.prober as cfg
from src.config.global_config import __version__
from src.taxonomy.Errors import TaxonomyParseError
from src.network.RequestFailError import RequestFailError
from src.taxonomy.TaxonomySearcher import TaxonomySearcher
from src.config.prober import PACKET_MODE_0, PACKET_MODE_1


class ProberArgs:
    def __init__(self,
                 input_fpaths : Sequence[str],
                 output_dirpath : str,
                 probing_batch_size : int,
                 packet_mode : str,
                 packet_size : int,
                 max_seq_len : int,
                 blast_algorithm : str,
                 organisms : Sequence[int],
                 phred_offset : int):
        self.input_fpaths       = input_fpaths
        self.output_dirpath     = output_dirpath
        self.probing_batch_size = probing_batch_size
        self.packet_mode        = packet_mode
        self.packet_size        = packet_size
        self.max_seq_len        = max_seq_len
        self.blast_algorithm    = blast_algorithm
        self.organisms          = organisms
        self.phred_offset       = phred_offset
    # end def

    def __str__(self) -> str:
        return f'''
    input_fpaths:       {self.input_fpaths},
    output_dirpath:     {self.output_dirpath},
    probing_batch_size: {self.probing_batch_size},
    packet_mode:        {self.packet_mode},
    packet_size:        {self.packet_size},
    max_seq_len:        {self.max_seq_len},
    blast_algorithm:    {self.blast_algorithm},
    organisms:          {self.organisms},
    phred_offset:       {self.phred_offset}.\n'''
        # end def

    def __repr__(self):
        return f'''ProberArgs(
    input_fpaths={self.input_fpaths!r},
    output_dirpath={self.output_dirpath!r},
    probing_batch_size={self.probing_batch_size!r},
    packet_mode={self.packet_mode!r},
    packet_size={self.packet_size!r},
    max_seq_len={self.max_seq_len!r},
    blast_algorithm={self.blast_algorithm!r},
    organisms={self.organisms!r},
    phred_offset={self.phred_offset!r}
)'''
    # end def
# end class


class ProberArgsParser:

    def parse(self) -> ProberArgs:
        raw_args = self._parse_raw_args()
        return ProberArgs(
            input_fpaths=self._parse_input_fpaths(raw_args),
            output_dirpath=self._parse_outdir_arg(raw_args),
            probing_batch_size=self._parse_int_gt0_arg(
                raw_args,
                'probing_batch_size'
            ),
            packet_mode=self._parse_packet_mode(raw_args),
            packet_size=self._parse_int_gt0_arg(
                raw_args,
                'packet_size'
            ),
            max_seq_len=self._parse_int_gt0_arg(
                raw_args,
                'max_seq_len'
            ),
            blast_algorithm=self._parse_blast_algorithm(raw_args),
            organisms=self._parse_organisms(raw_args),
            phred_offset=self._parse_int_gt0_arg(
                raw_args,
                'phred_offset'
            )
        )
    # end def

    def _parse_raw_args(self) -> argparse.Namespace:
        # TODO RELEASE: add description, epilog
        parser = argparse.ArgumentParser(
            prog='barapost2-prober'#,
            # description='What the program does',
            # epilog='Text at the bottom of help'
        )

        parser.add_argument(
            '-v',
            '--version',
            required=False,
            help='Print version and exit.',
            action='store_true'
        )
        parser.add_argument(
            'input_files',
            nargs='*',
            help='Input FASTA or FASTQ files.'
        )
        parser.add_argument(
            '-d',
            '--indir',
            help='A directory containing input FASTA or FASTQ files.'
        )
        parser.add_argument(
            '-b',
            '--probing-batch-size',
            type=int,
            default=cfg.DEFAULT_PROBING_BATCH_SIZE,
            help='TODO: add help.'
        )
        parser.add_argument(
            '-p',
            '--packet-size',
            type=int,
            default=cfg.DEFAULT_PACKET_SIZE,
            help='TODO: add help.'
        )
        parser.add_argument(
            '-c',
            '--packet-mode',
            default=cfg.DEFAULT_PACKET_MODE,
            help='TODO: add help.'
        )
        parser.add_argument(
            '-a',
            '--algorithm',
            default=cfg.DEFAULT_BLAST_ALGORITHM,
            help='BLAST algorithm to use.'
        )
        parser.add_argument(
            '-g',
            '--organisms',
            nargs='*',
            help='TaxIDs of organisms to align the input sequences against.'
        )
        parser.add_argument(
            '-x',
            '--max-seq-len',
            type=int,
            help='TODO: add help.'
        )
        parser.add_argument(
            '--phred-offset',
            default=cfg.DEFAULT_PHRED_OFFSET,
            type=int,
            help='TODO: add help.'
        )
        parser.add_argument(
            '-o',
            '--outdir',
            default=cfg.DEFAULT_OUTDIR_PATH,
            help='Output directory'
        )

        args = parser.parse_args()

        if args.version:
            sys.stderr.write('{}\n'.format(__version__))
            sys.exit(0)
        # end if

        return args
    # end def

    def _parse_input_fpaths(self,
                            raw_args : argparse.Namespace) -> Sequence[str]:
        input_fpaths = raw_args.input_files
        if raw_args.indir is not None:
            input_fpaths = input_fpaths + self._parse_indir_argument(raw_args)
        # end if
        input_fpaths = sorted(
            frozenset(
                map(os.path.abspath, input_fpaths)
            )
        )
        for fpath in input_fpaths:
            if not os.path.isfile(fpath):
                sys.stderr.write('Error: file `{}` does not exits\n'.format(fpath))
                sys.exit(1)
            # end if
        # end for
        if len(input_fpaths) == 0:
            sys.stderr.write('Error: no input files detected\n')
            sys.stderr.write('Please specify them as positional arguments\n')
            sys.stderr.write('  or using the `-d` option.\n')
            sys.exit(1)
        # end if
        return input_fpaths
    # end def

    def _parse_indir_argument(self,
                              raw_args : argparse.Namespace) -> Sequence[str]:
        indir_path = raw_args.indir
        if not os.path.isdir(indir_path):
            sys.stderr.write('Error: directory `{}` does not exits\n'.format(indir_path))
            sys.exit(1)
        # end if

        all_indir_fpaths = glob.iglob(
            os.path.join(indir_path, '*')
        )
        hts_indir_fpaths = list(filter(
            lambda f: fs.is_fasta(f) or fs.is_fastq(f),
            all_indir_fpaths
        ))
        return hts_indir_fpaths
    # end def

    def _parse_outdir_arg(self, raw_args : argparse.Namespace) -> str:
        return os.path.abspath(raw_args.outdir)
    # end def

    def _parse_int_gt0_arg(self,
                           raw_args : argparse.Namespace,
                           arg_name : str) -> int:
        arg_value = getattr(raw_args, arg_name, None)
        if arg_value is None:
            return None
        # end if

        try:
            arg_value_int = int(arg_value)
            if arg_value_int < 1:
                raise ValueError
            # end if
        except ValueError:
            err_msg = (
                'Error: {} value is invalid: "{}". '
                'It must be a positive integer.\n'
            ).format(arg_name, arg_value)
            sys.stderr.write(err_msg)
            sys.exit(1)
        # end try

        return arg_value_int
    # end def

    def _parse_packet_mode(self, raw_args : argparse.Namespace) -> str:
        packet_mode = raw_args.packet_mode
        allowed_modes = (PACKET_MODE_0, PACKET_MODE_1)
        if packet_mode not in allowed_modes:
            allowed_str = ', '.join(
                list(map(
                    lambda x: f'`{x}`',
                    allowed_modes
                ))
            )
            msg = (
                'Error: invalid packet mode: "{}". '
                'Allowed modes: {}.\n'
            ).format(packet_mode, allowed_str)
            sys.stderr.write(msg)
            sys.exit(1)
        # end if
        return packet_mode
    # end def


    def _parse_blast_algorithm(self, raw_args : argparse.Namespace) -> str:
        algorithm_key = raw_args.algorithm

        try:
            blast_algorithm = cfg.BLAST_ALGORITHMS[algorithm_key]
        except KeyError:
            allowed_str = ', '.join(
                list(map(
                    lambda x: f'`{x}`',
                    cfg.BLAST_ALGORITHMS.keys()
                ))
            )
            msg = (
                'Error: invalid blast algorithm argument: "{}". '
                'Allowed values: {}.\n'
            ).format(algorithm_key, allowed_str)
            sys.stderr.write(msg)
            sys.exit(1)
        # end try

        return blast_algorithm
    # end def

    def _parse_organisms(self, raw_args : argparse.Namespace) -> Sequence[str]:
        taxids = raw_args.organisms
        if taxids is None or len(taxids) == 0:
            return taxids
        # end if
        self._validate_taxids(taxids)
        return taxids
    # end def

    def _validate_taxids(self, taxids):
        numeric_pattern = re.compile(r'[1-9][0-9]*')
        for taxid in taxids:
            if re.match(numeric_pattern, taxid) is None:
                sys.stderr.write(
                    'Error: invalid TaxID: "{}". It must be an integer.\n'.format(taxid)
                )
                sys.exit(1)
            # end if
        # end for

        sys.stderr.write('Verifying TaxIDs\n')
        tax_searcher = TaxonomySearcher()
        for taxid in taxids:
            try:
                taxonomy = tax_searcher.tax_id2taxonomy(taxid)
            except (TaxonomyParseError, RequestFailError):
                msg = (
                    'Error: cannot find taxonomy info for TaxID "{}". '
                    'Please check this TaxID: it might be incorrect '
                    '(https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi).\n'
                ).format(taxid)
                sys.stderr.write(msg)
                sys.exit(1)
            else:
                sys.stderr.write('  {} - {}\n'.format(taxid, taxonomy.tax_name))
            # end for
        # end for
    # end def
# end class
