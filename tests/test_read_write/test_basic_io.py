
import os
from typing import Sequence

import pytest

from src.containers.SeqRecord import SeqRecord
from src.reader_system.ReaderWrapper import ReaderWrapper
from src.writer_system.WriterWrapper import WriterWrapper
from src.containers.ClassifContainer import ClassifContainer

import tests.util as util
from tests.test_read_write.fixtures import some_plain_fasta_fpath, \
                                           some_gzipped_fasta_fpath, \
                                           some_plain_fastq_fpath, \
                                           some_gzipped_fastq_fpath, \
                                           some_pod5_fpath, \
                                           some_fast5_fpath, \
                                           tmp_output_dir_path, \
                                           mock_classif_label
                                           # TODO: S/BLOW5 is to be implemented later
                                           # some_blow5_fpath, \
                                           # some_slow5_fpath, \


class TestBasicIO:

    def test_basic_fasta_io(self,
                            some_plain_fasta_fpath,
                            tmp_output_dir_path,
                            mock_classif_label):
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
        # end with)

        expected_outfpath = _make_expected_mock_outfpath(
            tmp_output_dir_path,
            mock_classif_label,
            'fasta'
        )

        assert os.path.exists(expected_outfpath) == True

        expected_sum = util.md5_file_sum(some_plain_fasta_fpath)
        observed_sum = util.md5_file_sum(expected_outfpath)
        assert expected_sum == observed_sum
    # end def

    def test_gzipped_fasta_io(self,
                              some_gzipped_fasta_fpath,
                              tmp_output_dir_path,
                              mock_classif_label):
        util.clear_dir(tmp_output_dir_path)

        reader = ReaderWrapper(
            file_paths=[some_gzipped_fasta_fpath]
        )
        writer = WriterWrapper(
            outdir_path=tmp_output_dir_path,
            _type_='fasta',
            _gzip_=True,
            line_width=60
        )

        with reader as input_handle, \
             writer as output_handle:
            for packet in input_handle:
                classified_packet = _mock_classify(packet)
                output_handle.write(classified_packet)
            # end for
        # end with)

        expected_outfpath = _make_expected_mock_outfpath(
            tmp_output_dir_path,
            mock_classif_label,
            'fasta.gz'
        )

        assert os.path.exists(expected_outfpath) == True

        expected_sum = util.md5_gzipped_file_sum(some_gzipped_fasta_fpath)
        observed_sum = util.md5_gzipped_file_sum(expected_outfpath)
        assert expected_sum == observed_sum
    # end def

    def test_basic_fastq_io(self,
                            some_plain_fastq_fpath,
                            tmp_output_dir_path,
                            mock_classif_label):
        util.clear_dir(tmp_output_dir_path)

        reader = ReaderWrapper(
            file_paths=[some_plain_fastq_fpath]
        )
        writer = WriterWrapper(
            outdir_path=tmp_output_dir_path,
            _type_='fastq'
        )

        with reader as input_handle, \
             writer as output_handle:
            for packet in input_handle:
                classified_packet = _mock_classify(packet)
                output_handle.write(classified_packet)
            # end for
        # end with)

        expected_outfpath = _make_expected_mock_outfpath(
            tmp_output_dir_path,
            mock_classif_label,
            'fastq'
        )

        assert os.path.exists(expected_outfpath) == True

        expected_sum = util.md5_file_sum(some_plain_fastq_fpath)
        observed_sum = util.md5_file_sum(expected_outfpath)
        assert expected_sum == observed_sum
    # end def

    def test_gzipped_fastq_io(self,
                              some_gzipped_fastq_fpath,
                              tmp_output_dir_path,
                              mock_classif_label):
        util.clear_dir(tmp_output_dir_path)

        reader = ReaderWrapper(
            file_paths=[some_gzipped_fastq_fpath]
        )
        writer = WriterWrapper(
            outdir_path=tmp_output_dir_path,
            _type_='fastq',
            _gzip_=True
        )

        with reader as input_handle, \
             writer as output_handle:
            for packet in input_handle:
                classified_packet = _mock_classify(packet)
                output_handle.write(classified_packet)
            # end for
        # end with)

        expected_outfpath = _make_expected_mock_outfpath(
            tmp_output_dir_path,
            mock_classif_label,
            'fastq.gz'
        )

        assert os.path.exists(expected_outfpath) == True

        expected_sum = util.md5_gzipped_file_sum(some_gzipped_fastq_fpath)
        observed_sum = util.md5_gzipped_file_sum(expected_outfpath)
        assert expected_sum == observed_sum
    # end def

    def test_pod5_io(self,
                     some_pod5_fpath,
                     tmp_output_dir_path,
                     mock_classif_label):
        util.clear_dir(tmp_output_dir_path)

        reader = ReaderWrapper(
            file_paths=[some_pod5_fpath]
        )
        writer = WriterWrapper(
            outdir_path=tmp_output_dir_path,
            _type_='pod5'
        )

        with reader as input_handle, \
             writer as output_handle:
            for packet in input_handle:
                classified_packet = _mock_classify(packet)
                output_handle.write(classified_packet)
            # end for
        # end with)

        expected_outfpath = _make_expected_mock_outfpath(
            tmp_output_dir_path,
            mock_classif_label,
            'pod5'
        )

        assert os.path.exists(expected_outfpath) == True

        expected_sum = util.md5_pod5_file(some_pod5_fpath)
        observed_sum = util.md5_pod5_file(expected_outfpath)
        assert expected_sum == observed_sum
    # end def

    def test_fast5_io(self,
                      some_fast5_fpath,
                      tmp_output_dir_path,
                      mock_classif_label):
        util.clear_dir(tmp_output_dir_path)

        reader = ReaderWrapper(
            file_paths=[some_fast5_fpath]
        )
        writer = WriterWrapper(
            outdir_path=tmp_output_dir_path,
            _type_='fast5'
        )

        with reader as input_handle, \
             writer as output_handle:
            for packet in input_handle:
                classified_packet = _mock_classify(packet)
                output_handle.write(classified_packet)
            # end for
        # end with)

        expected_outfpath = _make_expected_mock_outfpath(
            tmp_output_dir_path,
            mock_classif_label,
            'fast5'
        )

        assert os.path.exists(expected_outfpath) == True

        expected_sum = util.md5_fast5_file(some_fast5_fpath)
        observed_sum = util.md5_fast5_file(expected_outfpath)
        assert expected_sum == observed_sum
    # end def

    # TODO: S/BLOW5 is to be implemented later
    # The test fails:
    # write_record: slow5_aux_add_enum end_reason: 4 could not set to C s5.header.aux_meta struct
    # write_record: slow5_aux_add_enum end_reason: 4 could not set to C s5.header.aux_meta struct
    # write_record: aux_meta fields failed to initialise
    # write_record: aux_meta fields failed to initialise
    # And many more similar errors

    # def test_blow5_io(self,
    #                   some_blow5_fpath,
    #                   tmp_output_dir_path,
    #                   mock_classif_label):
    #     util.clear_dir(tmp_output_dir_path)

    #     reader = ReaderWrapper(
    #         file_paths=[some_blow5_fpath]
    #     )
    #     writer = WriterWrapper(
    #         outdir_path=tmp_output_dir_path,
    #         _type_='blow5'
    #     )

    #     with reader as input_handle, \
    #          writer as output_handle:
    #         for packet in input_handle:
    #             classified_packet = _mock_classify(packet)
    #             output_handle.write(classified_packet)
    #         # end for
    #     # end with)

    #     expected_outfpath = _make_expected_mock_outfpath(
    #         tmp_output_dir_path,
    #         mock_classif_label,
    #         'blow5'
    #     )

    #     assert os.path.exists(expected_outfpath) == True

    #     expected_sum = util.md5_file_sum(some_blow5_fpath)
    #     observed_sum = util.md5_file_sum(expected_outfpath)
    #     assert expected_sum == observed_sum
    # # end def
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
                                 extenstion : str) -> str:
    return os.path.join(
        outdir_path,
        '{}_0.{}'.format(label, extenstion)
    )
# end def
