
import pytest

from src.reader_system.ReaderWrapper import ReaderWrapper

from tests.test_read_write.fixtures import some_plain_fasta_fpath, \
                                           some_gzipped_fasta_fpath, \
                                           some_plain_fastq_fpath, \
                                           some_gzipped_fastq_fpath, \
                                           some_pod5_fpath, \
                                           some_fast5_fpath
                                           # TODO: LATER: S/BLOW5 is to be implemented later
                                           # some_blow5_fpath, \
                                           # some_slow5_fpath, \


class TestCountRecordsInCurrFile:

    def test_plain_fasta(self, some_plain_fasta_fpath : str):
        expected_record_count = 8

        reader = ReaderWrapper(
            file_paths=[some_plain_fasta_fpath]
        )
        with reader as input_handle:
            observed_record_count = input_handle._count_records_in_curr_file()
        # end def

        assert observed_record_count == expected_record_count
    # end def

    def test_gzipped_fasta(self, some_gzipped_fasta_fpath : str):
        expected_record_count = 7

        reader = ReaderWrapper(
            file_paths=[some_gzipped_fasta_fpath]
        )
        with reader as input_handle:
            observed_record_count = input_handle._count_records_in_curr_file()
        # end def

        assert observed_record_count == expected_record_count
    # end def

    def test_plain_fastq(self, some_plain_fastq_fpath : str):
        expected_record_count = 7

        reader = ReaderWrapper(
            file_paths=[some_plain_fastq_fpath]
        )
        with reader as input_handle:
            observed_record_count = input_handle._count_records_in_curr_file()
        # end def

        assert observed_record_count == expected_record_count
    # end def

    def test_gzipped_fastq(self, some_gzipped_fastq_fpath : str):
        expected_record_count = 7

        reader = ReaderWrapper(
            file_paths=[some_gzipped_fastq_fpath]
        )
        with reader as input_handle:
            observed_record_count = input_handle._count_records_in_curr_file()
        # end def

        assert observed_record_count == expected_record_count
    # end def

    def test_fast5(self, some_fast5_fpath : str):
        expected_record_count = 4

        reader = ReaderWrapper(
            file_paths=[some_fast5_fpath]
        )
        with reader as input_handle:
            observed_record_count = input_handle._count_records_in_curr_file()
        # end def

        assert observed_record_count == expected_record_count
    # end def

    def test_fast5(self, some_pod5_fpath : str):
        expected_record_count = 4

        reader = ReaderWrapper(
            file_paths=[some_pod5_fpath]
        )
        with reader as input_handle:
            observed_record_count = input_handle._count_records_in_curr_file()
        # end def

        assert observed_record_count == expected_record_count
    # end def
# end class
