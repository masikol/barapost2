
import os

import pytest

from src.reader_system.ReaderWrapper import ReaderWrapper

from tests.test_read_write.fixtures import some_plain_fasta_fpath, \
                                           some_gzipped_fasta_fpath


class TestPacketSizeSeqCountMode:

    def test_packet_size_of_one(self, some_plain_fasta_fpath : str):

        packet_size = 1

        reader = ReaderWrapper(
            file_paths=[some_plain_fasta_fpath],
            packet_size=packet_size
        )

        with reader as input_handle:
            for seq_packet in input_handle:
                assert len(seq_packet) == packet_size
            # end for
        # end with
    # end def


    def test_packet_size_is_multiple(self, some_plain_fasta_fpath : str):
        # Here, packet_size is a multiple of the number of seqs
        #   in the test input file

        packet_size = 2

        reader = ReaderWrapper(
            file_paths=[some_plain_fasta_fpath],
            packet_size=packet_size
        )

        with reader as input_handle:
            for seq_packet in input_handle:
                assert len(seq_packet) == packet_size
            # end for
        # end with
    # end def


    def test_packet_size_is_not_multiple(self, some_plain_fasta_fpath : str):
        # Here, packet_size is NOT a multiple of the number of seqs
        #   in the test input file

        packet_size = 3

        reader = ReaderWrapper(
            file_paths=[some_plain_fasta_fpath],
            packet_size=packet_size
        )

        packet_sizes_obtained = list()

        with reader as input_handle:
            for seq_packet in input_handle:
                packet_sizes_obtained.append(
                    len(seq_packet)
                )
            # end for
        # end with

        packet_sizes_expected = [3, 3, 2]
        assert packet_sizes_expected == packet_sizes_obtained
    # end def


    def test_packet_size_more_than_num_seqs(self, some_plain_fasta_fpath : str):
        # Here, packet_size is more than the number of seqs
        #   in the test input file

        packet_size = 19

        reader = ReaderWrapper(
            file_paths=[some_plain_fasta_fpath],
            packet_size=packet_size
        )

        with reader as input_handle:
            seq_packets = [p for p in input_handle]
        # end with

        assert len(seq_packets) == 1
        assert len(next(iter(seq_packets))) == 8 # total num of seqs in the test input file
    # end def


    def test_packet_size_skip_n_first_seqs(self, some_plain_fasta_fpath : str):
        # Here, we test if n_first_skip_dict distorts packet_size

        packet_size = 3

        n = 3
        n_first_skip_dict = {
            os.path.basename(some_plain_fasta_fpath) : n,
        }

        reader = ReaderWrapper(
            file_paths=[some_plain_fasta_fpath],
            packet_size=packet_size,
            n_first_skip_dict=n_first_skip_dict
        )

        packet_sizes_obtained = list()

        with reader as input_handle:
            for seq_packet in input_handle:
                packet_sizes_obtained.append(
                    len(seq_packet)
                )
            # end for
        # end with

        packet_sizes_expected = [3, 2,]
        assert packet_sizes_expected == packet_sizes_obtained
    # end def


    def test_packet_size_multiple_files_is_multiple(self,
                                                    some_plain_fasta_fpath : str,
                                                    some_gzipped_fasta_fpath : str):
        # Here, packet_size is a multiple of the number of seqs
        #   in the first test input file
        packet_size = 4

        reader = ReaderWrapper(
            file_paths=[
                some_plain_fasta_fpath,
                some_gzipped_fasta_fpath,
            ],
            packet_size=packet_size
        )

        packet_sizes_obtained = list()

        with reader as input_handle:
            for seq_packet in input_handle:
                packet_sizes_obtained.append(
                    len(seq_packet)
                )
            # end for
        # end with

        packet_sizes_expected = [4, 4, 4, 3]
        assert packet_sizes_expected == packet_sizes_obtained
    # end def


    def test_packet_size_multiple_files_is_not_multiple(self,
                                                        some_plain_fasta_fpath : str,
                                                        some_gzipped_fasta_fpath : str):
        # Here, packet_size is NOT a multiple of the number of seqs
        #   in the first test input file
        packet_size = 3

        reader = ReaderWrapper(
            file_paths=[
                some_plain_fasta_fpath,
                some_gzipped_fasta_fpath,
            ],
            packet_size=packet_size
        )

        packet_sizes_obtained = list()

        with reader as input_handle:
            for seq_packet in input_handle:
                packet_sizes_obtained.append(
                    len(seq_packet)
                )
            # end for
        # end with

        packet_sizes_expected = [3, 3, 2, 3, 3, 1]
        assert packet_sizes_expected == packet_sizes_obtained
    # end def
# end class


class TestPacketSizeSumSeqLenMode:
    # Here, we test packet size if packet_mode is sum_seq_len
    # Lengths of the test sequences:
    # NODE_1_length_26183_cov_2.977840: 1020 bp
    # NODE_2_length_11992_cov_2.917567:  960 bp
    # NODE_3_length_11322_cov_3.701606: 1180 bp
    # NODE_4_length_10922_cov_4.052544: 1000 bp
    # NODE_5_length_10759_cov_4.271020: 1000 bp
    # NODE_6_length_10324_cov_3.083552: 1000 bp
    # NODE_7_length_10236_cov_4.014832: 1000 bp
    # NODE_426383_length_56_cov_3.000000: 56 bp

    def test_packet_size_simple(self,
                                some_plain_fasta_fpath : str):
        packet_mode = 'sum_seq_len'
        packet_size = 2000

        reader = ReaderWrapper(
            file_paths=[
                some_plain_fasta_fpath,
            ],
            packet_mode=packet_mode,
            packet_size=packet_size
        )

        packet_sizes_obtained = list()

        with reader as input_handle:
            for seq_packet in input_handle:
                packet_sizes_obtained.append(
                    len(seq_packet)
                )
            # end for
        # end with

        packet_sizes_expected = [3, 2, 2, 1]
        assert packet_sizes_expected == packet_sizes_obtained
    # end def


    def test_packet_size_with_max_seq_len(self,
                                some_plain_fasta_fpath : str):
        packet_mode = 'sum_seq_len'
        packet_size = 1200
        max_seq_len = 500

        reader = ReaderWrapper(
            file_paths=[
                some_plain_fasta_fpath,
            ],
            packet_mode=packet_mode,
            packet_size=packet_size,
            max_seq_len=max_seq_len
        )

        packet_sizes_obtained = list()

        with reader as input_handle:
            for seq_packet in input_handle:
                packet_sizes_obtained.append(
                    len(seq_packet)
                )
            # end for
        # end with

        packet_sizes_expected = [3, 3, 2]
        assert packet_sizes_expected == packet_sizes_obtained
    # end def
# end class
