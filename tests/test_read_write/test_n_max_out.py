
import os
import glob
from typing import Sequence

import pytest

from src.containers.SeqRecord import SeqRecord
from src.reader_system.ReaderWrapper import ReaderWrapper
from src.writer_system.WriterWrapper import WriterWrapper
from src.containers.ClassifContainer import ClassifContainer

import tests.util as util
from tests.test_read_write.fixtures import some_plain_fasta_fpath, \
                                           some_pod5_fpath, \
                                           some_fast5_fpath, \
                                           tmp_output_dir_path, \
                                           mock_classif_label


class TestNMaxOut:

    def test_default_n_max_out(self,
                               some_plain_fasta_fpath : str,
                               tmp_output_dir_path : str,
                               mock_classif_label : str):

        util.clear_dir(tmp_output_dir_path)

        reader = ReaderWrapper(
            file_paths=[some_plain_fasta_fpath]
        )
        writer = WriterWrapper(
            outdir_path=tmp_output_dir_path,
            _type_='fasta',
            line_width=60 # the test input file has line width of 60 chars
        )

        with reader as input_handle, \
             writer as output_handle:
            for packet in input_handle:
                classified_packet = _mock_classify(packet)
                output_handle.write(classified_packet)
            # end for
        # end with

        expected_outfpath = _make_expected_mock_outfpath(
            tmp_output_dir_path,
            mock_classif_label,
            0,
            'fasta'
        )

        expected_record_count = 8 # total record count in the input file
        observed_record_count = self._count_fasta_records(expected_outfpath)

        assert observed_record_count == expected_record_count
    # end def


    def test_n_max_out_is_multiple(self,
                                   some_plain_fasta_fpath : str,
                                   tmp_output_dir_path : str,
                                   mock_classif_label : str):
        # Here, n is a multiple of the number of records in the input file

        util.clear_dir(tmp_output_dir_path)

        reader = ReaderWrapper(
            file_paths=[some_plain_fasta_fpath]
        )
        writer = WriterWrapper(
            outdir_path=tmp_output_dir_path,
            _type_='fasta',
            n_max_out=4,
            line_width=60 # the test input file has line width of 60 chars
        )

        with reader as input_handle, \
             writer as output_handle:
            for packet in input_handle:
                classified_packet = _mock_classify(packet)
                output_handle.write(classified_packet)
            # end for
        # end with

        expected_out_file_count = 2
        observed_out_file_count = len(
            glob.glob(
                os.path.join(tmp_output_dir_path, '*.fasta')
            )
        )
        assert observed_out_file_count == expected_out_file_count

        expected_outfpaths = [
            _make_expected_mock_outfpath(
                tmp_output_dir_path,
                mock_classif_label,
                i,
                'fasta'
            )
            for i in (0, 1)
        ]
        observed_record_counts = tuple(
            (
                self._count_fasta_records(f)
                for f in expected_outfpaths
            )
        )

        expected_record_counts = (4, 4)
        assert observed_record_counts == expected_record_counts
    # end def


    def test_n_max_out_is_not_multiple(self,
                                       some_plain_fasta_fpath : str,
                                       tmp_output_dir_path : str,
                                       mock_classif_label : str):
        # Here, n is not a multiple of the number of records in the input file

        util.clear_dir(tmp_output_dir_path)

        reader = ReaderWrapper(
            file_paths=[some_plain_fasta_fpath]
        )
        writer = WriterWrapper(
            outdir_path=tmp_output_dir_path,
            _type_='fasta',
            n_max_out=3,
            line_width=60 # the test input file has line width of 60 chars
        )

        with reader as input_handle, \
             writer as output_handle:
            for packet in input_handle:
                classified_packet = _mock_classify(packet)
                output_handle.write(classified_packet)
            # end for
        # end with

        expected_out_file_count = 3
        observed_out_file_count = len(
            glob.glob(
                os.path.join(tmp_output_dir_path, '*.fasta')
            )
        )
        assert observed_out_file_count == expected_out_file_count

        expected_outfpaths = [
            _make_expected_mock_outfpath(
                tmp_output_dir_path,
                mock_classif_label,
                i,
                'fasta'
            )
            for i in (0, 1, 2,)
        ]
        observed_record_counts = tuple(
            (
                self._count_fasta_records(f)
                for f in expected_outfpaths
            )
        )

        expected_record_counts = (3, 3, 2)
        assert observed_record_counts == expected_record_counts
    # end def


    def test_n_max_out_is_multiple_pod5(self,
                                        some_pod5_fpath : str,
                                        tmp_output_dir_path : str,
                                        mock_classif_label : str):
        # Here, n is a multiple of the number of records in the input file.
        # This separate test for POD5 to test if empty output POD5 files
        #   get closed properly. We do not count POD5 records intentionally:
        #   we believe if it works for FASTA, it works for every format.

        util.clear_dir(tmp_output_dir_path)

        reader = ReaderWrapper(
            file_paths=[some_pod5_fpath]
        )
        writer = WriterWrapper(
            outdir_path=tmp_output_dir_path,
            _type_='pod5',
            n_max_out=2,
        )

        with reader as input_handle, \
             writer as output_handle:
            for packet in input_handle:
                classified_packet = _mock_classify(packet)
                output_handle.write(classified_packet)
            # end for
        # end with

        expected_out_file_count = 2
        observed_out_file_count = len(
            glob.glob(
                os.path.join(tmp_output_dir_path, '*.pod5')
            )
        )
        assert observed_out_file_count == expected_out_file_count
    # end def


    def test_n_max_out_is_multiple_fast5(self,
                                         some_fast5_fpath : str,
                                         tmp_output_dir_path : str,
                                         mock_classif_label : str):
        # Here, n is a multiple of the number of records in the input file.
        # This separate test for FAST5 to test if empty output FAST5 files
        #   get closed properly. We do not count FAST5 records intentionally:
        #   we believe if it works for FASTA, it works for every format.

        util.clear_dir(tmp_output_dir_path)

        reader = ReaderWrapper(
            file_paths=[some_fast5_fpath]
        )
        writer = WriterWrapper(
            outdir_path=tmp_output_dir_path,
            _type_='fast5',
            n_max_out=2,
        )

        with reader as input_handle, \
             writer as output_handle:
            for packet in input_handle:
                classified_packet = _mock_classify(packet)
                output_handle.write(classified_packet)
            # end for
        # end with

        expected_out_file_count = 2
        observed_out_file_count = len(
            glob.glob(
                os.path.join(tmp_output_dir_path, '*.fast5')
            )
        )
        assert observed_out_file_count == expected_out_file_count
    # end def


    def _count_fasta_records(self, fasta_fpath : str):
        with open(fasta_fpath, 'rt') as input_handle:
            record_count = input_handle.read().count('>')
        # end with
        return record_count
    # end def
# end class


def _mock_classify(seq_packet : Sequence[SeqRecord]) -> Sequence[ClassifContainer]:
    return tuple(
        map(
            _mock_classify_single,
            seq_packet
        )
    )
# end def

def _mock_classify_single(seq_record : SeqRecord) -> ClassifContainer:
    return ClassifContainer(
        record=seq_record,
        label='test'
    )
# end def

def _make_expected_mock_outfpath(outdir_path : str,
                                 label : str,
                                 number : int,
                                 extenstion : str) -> str:
    return os.path.join(
        outdir_path,
        '{}_{}.{}'.format(label, number, extenstion)
    )
# end def
