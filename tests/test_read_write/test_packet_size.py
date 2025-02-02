
import pytest

from src.reader_system.ReaderWrapper import ReaderWrapper

from tests.test_read_write.fixtures import some_plain_fasta_fpath, \
                                           some_gzipped_fasta_fpath


class TestPacketSize:

    def test_packet_size_of_one(self, some_plain_fasta_fpath):

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


    def test_packet_size_is_multiple(self, some_plain_fasta_fpath):
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


    def test_packet_size_is_not_multiple(self, some_plain_fasta_fpath):
        # Here, packet_size is NOT a multiple of the number of seqs
        #   in the test input file

        packet_size = 3

        reader = ReaderWrapper(
            file_paths=[some_plain_fasta_fpath],
            packet_size=packet_size
        )

        packet_sizes_expected = [3, 3, 2]
        packet_sizes_obtained = list()

        with reader as input_handle:
            for seq_packet in input_handle:
                packet_sizes_obtained.append(
                    len(seq_packet)
                )
            # end for
        # end with

        assert packet_sizes_expected == packet_sizes_obtained
    # end def


    def test_packet_size_more_than_num_seqs(self, some_plain_fasta_fpath):
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
# end class
