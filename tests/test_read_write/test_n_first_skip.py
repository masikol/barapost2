
import os

import pytest

from src.reader_system.ReaderWrapper import ReaderWrapper

from tests.test_read_write.fixtures import some_plain_fasta_fpath, \
                                           some_gzipped_fasta_fpath


class TestNFirstSkip:

    def test_skip_lt_record_count(self,
                                  some_plain_fasta_fpath : str):
        n = 5
        n_first_skip_dict = {
            os.path.basename(some_plain_fasta_fpath) : n,
        }

        reader = ReaderWrapper(
            file_paths=[
                some_plain_fasta_fpath,
            ],
            packet_size=1000, # some large number to read them all
            n_first_skip_dict=n_first_skip_dict
        )

        with reader as input_handle:
            single_packet = next(iter(input_handle))
        # end with

        num_records_expected = 8 - n # 8 records in the test fasta file
        num_records_obtained = len(single_packet)

        assert num_records_obtained == num_records_expected
    # end def

    def test_skip_eq_record_count(self,
                                  some_plain_fasta_fpath : str):
        n = 8
        n_first_skip_dict = {
            os.path.basename(some_plain_fasta_fpath) : n,
        }

        reader = ReaderWrapper(
            file_paths=[
                some_plain_fasta_fpath,
            ],
            packet_size=1000, # some large number to read them all
            n_first_skip_dict=n_first_skip_dict
        )

        with reader as input_handle:
            seq_packets = [p for p in input_handle]
        # end with

        num_records_expected = 0
        num_records_obtained = len(seq_packets)

        assert num_records_obtained == num_records_expected
    # end def

    def test_skip_gt_record_count(self,
                                  some_plain_fasta_fpath : str):
        n = 9
        n_first_skip_dict = {
            os.path.basename(some_plain_fasta_fpath) : n,
        }

        reader = ReaderWrapper(
            file_paths=[
                some_plain_fasta_fpath,
            ],
            packet_size=1000, # some large number to read them all
            n_first_skip_dict=n_first_skip_dict
        )

        with reader as input_handle:
            seq_packets = [p for p in input_handle]
        # end with

        num_records_expected = 0
        num_records_obtained = len(seq_packets)

        assert num_records_obtained == num_records_expected
    # end def


    def test_skip_eq_record_count_milti_file(self,
                                             some_plain_fasta_fpath : str,
                                             some_gzipped_fasta_fpath : str):
        # Test winding to the second file if the first file
        #   is exhausted from the very beginning.
        n = 8 # total seq count in the first file
        n_first_skip_dict = {
            os.path.basename(some_plain_fasta_fpath) : n,
        }

        reader = ReaderWrapper(
            file_paths=[
                some_plain_fasta_fpath,
                some_gzipped_fasta_fpath,
            ],
            packet_size=1000, # some large number to read them all
            n_first_skip_dict=n_first_skip_dict
        )

        packet_concatenated = list()
        with reader as input_handle:
            for seq_packet in input_handle:
                packet_concatenated.extend(seq_packet)
            # end for
        # end with

        num_records_expected = 7 # total seq count in the second file
        num_records_obtained = len(packet_concatenated)

        assert num_records_obtained == num_records_expected
    # end def

# end def
