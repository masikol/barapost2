
import pytest

from src.reader_system.ReaderWrapper import ReaderWrapper
from tests.test_read_write.fixtures import some_plain_fasta_fpath, \
                                           some_gzipped_fasta_fpath


class TestCurrInfpath:

    def test_curr_infpath_is_not_multiple(self,
                                          some_plain_fasta_fpath : str,
                                          some_gzipped_fasta_fpath : str):
        # Here, packet_size is NOT a multiple of the number of sequences
        #   in the first input file: some_plain_fasta_fpath
        reader = ReaderWrapper(
            file_paths=[
                some_plain_fasta_fpath,
                some_gzipped_fasta_fpath,
            ],
            packet_size = 5
        )

        with reader as input_handle:
            packer_iterator = iter(input_handle)

            _ = next(packer_iterator)
            assert input_handle.get_curr_infpath() == some_plain_fasta_fpath
            _ = next(packer_iterator)
            assert input_handle.get_curr_infpath() == some_plain_fasta_fpath

            _ = next(packer_iterator)
            assert input_handle.get_curr_infpath() == some_gzipped_fasta_fpath
            _ = next(packer_iterator)
            assert input_handle.get_curr_infpath() == some_gzipped_fasta_fpath
        # end with
    # end def

    def test_curr_infpath_is_multiple(self,
                                      some_plain_fasta_fpath : str,
                                      some_gzipped_fasta_fpath : str):
        # Here, packet_size is a multiple of the number of sequences
        #   in the first input file: some_plain_fasta_fpath
        reader = ReaderWrapper(
            file_paths=[
                some_plain_fasta_fpath,
                some_gzipped_fasta_fpath,
            ],
            packet_size = 4
        )

        with reader as input_handle:
            packer_iterator = iter(input_handle)

            _ = next(packer_iterator)
            assert input_handle.get_curr_infpath() == some_plain_fasta_fpath
            _ = next(packer_iterator)
            assert input_handle.get_curr_infpath() == some_plain_fasta_fpath

            _ = next(packer_iterator)
            assert input_handle.get_curr_infpath() == some_gzipped_fasta_fpath
            _ = next(packer_iterator)
            assert input_handle.get_curr_infpath() == some_gzipped_fasta_fpath
        # end with
    # end def

    def test_curr_infpath_n_first_skip(self,
                                       some_plain_fasta_fpath : str,
                                       some_gzipped_fasta_fpath : str):
        # Here, we will spik the first input file: some_plain_fasta_fpath
        reader = ReaderWrapper(
            file_paths=[
                some_plain_fasta_fpath,
                some_gzipped_fasta_fpath,
            ],
            packet_size = 5,
            n_first_skip_dict={
                some_plain_fasta_fpath : 8,
            }
        )

        with reader as input_handle:
            packer_iterator = iter(input_handle)

            _ = next(packer_iterator)
            assert input_handle.get_curr_infpath() == some_gzipped_fasta_fpath
            _ = next(packer_iterator)
            assert input_handle.get_curr_infpath() == some_gzipped_fasta_fpath
        # end with
    # end def
# end class
