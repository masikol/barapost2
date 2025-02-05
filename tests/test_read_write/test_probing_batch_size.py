
import os

import pytest

from src.reader_system.ReaderWrapper import ReaderWrapper

from tests.test_read_write.fixtures import some_plain_fasta_fpath, \
                                           some_gzipped_fasta_fpath


class TestProbingBatchSize:

    def test_default_probing_batch(self, some_plain_fasta_fpath : str):
        # Must read all records
        reader = ReaderWrapper(
            file_paths=[some_plain_fasta_fpath],
            packet_size=1000 # some large number to read them all
        )

        with reader as input_handle:
            seq_packet = next(iter(input_handle))
        # end with

        num_records_expected = 8 # total num of seqs in the test input file
        num_records_obtained = len(seq_packet)

        assert num_records_obtained == num_records_expected
    # end def

    def test_default_probing_batch_multiple_files(self,
                                                  some_plain_fasta_fpath : str,
                                                  some_gzipped_fasta_fpath : str):
        # Must read all records
        reader = ReaderWrapper(
            file_paths=[
                some_plain_fasta_fpath,
                some_gzipped_fasta_fpath
            ],
            packet_size=1000 # some large number to read them all
        )

        sum_of_packet_lengths = 0
        with reader as input_handle:
            for seq_packet in input_handle:
                sum_of_packet_lengths += len(seq_packet)
            # end for
        # end with

        num_records_expected = 8 + 7 # total num of seqs in the tow test input files
        num_records_obtained = sum_of_packet_lengths

        assert num_records_obtained == num_records_expected
    # end def


    def test_probing_batch(self, some_plain_fasta_fpath : str):
        probing_batch_size = 5
        reader = ReaderWrapper(
            file_paths=[some_plain_fasta_fpath],
            probing_batch_size=probing_batch_size,
            packet_size=1000 # some large number to read them all
        )

        with reader as input_handle:
            seq_packet = next(iter(input_handle))
        # end with

        num_records_expected = probing_batch_size
        num_records_obtained = len(seq_packet)

        assert num_records_obtained == num_records_expected
    # end def

    def test_probing_batch_multiple_files(self,
                                          some_plain_fasta_fpath : str,
                                          some_gzipped_fasta_fpath : str):
        probing_batch_size = 11
        reader = ReaderWrapper(
            file_paths=[
                some_plain_fasta_fpath,
                some_gzipped_fasta_fpath,
            ],
            probing_batch_size=probing_batch_size,
            packet_size=1000 # some large number to read them all
        )

        packet_concatenated = list()
        with reader as input_handle:
            for seq_packet in input_handle:
                packet_concatenated.extend(seq_packet)
            # end for
        # end with

        num_records_expected = probing_batch_size
        num_records_obtained = len(packet_concatenated)

        assert num_records_obtained == num_records_expected
    # end def

    def test_probing_batch_skip_first_n_seqs(self,
                                             some_plain_fasta_fpath : str):
        probing_batch_size = 7

        n = 5
        n_first_skip_dict = {
            os.path.basename(some_plain_fasta_fpath) : n,
        }

        reader = ReaderWrapper(
            file_paths=[
                some_plain_fasta_fpath,
            ],
            probing_batch_size=probing_batch_size,
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
# end class
