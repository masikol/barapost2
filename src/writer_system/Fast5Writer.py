
import os
import re
import logging

# TODO: remove
# from h5py import File
from ont_fast5_api.multi_fast5 import MultiFast5File
# TODO: remove
# from ont_fast5_api.fast5_interface import get_fast5_file

# TODO: remove
# from src.config.config import OUTPUT_DIR
from src.containers.Fast5 import Fast5
from src.writer_system.FileWriter import FileWriter


class Fast5Writer(FileWriter):

    def _write_single_record(self,
                             seq_record : Fast5,
                             out_file_handle : MultiFast5File):
        # TODO: remove
        # if self._detect_single_fast5(seq_record):
        #     # Single-FAST5 file
        #     self._copy_single_fast5_record(
        #         seq_record,
        #         out_file_handle
        #     )
        # else:
        #     # Multi-FAST5 file
        #     self._copy_multi_fast5_record(
        #         seq_record,
        #         out_file_handle
        #     )
        # # end if
        out_file_handle.add_existing_read(seq_record.read_data)
    # end def

    # TODO: remove
    # def _detect_single_fast5(self, seq_record):
    #     return 'Raw' in seq_record.file_handle.keys()
    # # end def

    # def _copy_multi_fast5_record(self, seq_record, out_file_handle):
    #     try:
    #         seq_record.file_handle.copy(seq_record.read_id, out_file_handle)
    #     except ValueError as err:
    #         # TODO handle this error properly
    #         logging.error(
    #             '''Error: `{}`
    #             The reason is probably the following:
    #             the read being copied to the output file is in this file already.
    #             ID of the read: `{}`
    #             Output file: `{}`''' \
    #             .format(str(err), read_name, to_f5.filename)
    #         )
    #     # end try
    # # end def

    # def _copy_single_fast5_record(self, seq_record, out_file_handle):
    #     read_group_name = seq_record.read_id
    #     in_file_handle = seq_record.file_handle
    #     # Create group in the destination multi_FAST5 file
    #     out_file_handle.create_group(read_group_name)

    #     # Copy "UniqueGlobalKey" to root of recently created group
    #     for ugk_subgr in in_file_handle['UniqueGlobalKey']:
    #         in_file_handle.copy(
    #             f'UniqueGlobalKey/{ugk_subgr}',
    #             out_file_handle[read_group_name]
    #         )
    #     # end for

    #     # Get data array in single-FAST5 file
    #     read_number_group = 'Raw/Reads/{}'.format(
    #         next(iter(in_file_handle['Raw']['Reads']))
    #     )
    #     # Copy the group to multi-FAST5 file
    #     in_file_handle.copy(
    #         in_file_handle[read_number_group],
    #         out_file_handle[read_group_name]
    #     )

    #     # Get read name in multi-FAST5 file
    #     # TODO: handle AttrubuteError
    #     read_number = re.search(
    #         r'(Read_[0-9]+)',
    #         read_number_group
    #     ).group(1)
    #     # Move data array to the "Raw" group, as it is in multi-FAST5 files
    #     out_file_handle.move(
    #         f'{read_group_name}/{read_number}',
    #         f'{read_group_name}/Raw'
    #     )

    #     # Copy everything else to recently created group
    #     for group in in_file_handle:
    #         if group != 'Raw' and group != 'UniqueGlobalKey':
    #             in_file_handle.copy(
    #                 group,
    #                 out_file_handle['/{}'.format(read_group_name)]
    #             )
    #         # end if
    #     # end for
    # # end def


    def _get_out_file_path(self, label : str, index : str) -> str:
        return os.path.join(
            self.outdir_path,
            f'{label}_{index}.{self.ext}'
        )
    # end def


    def _open_new_outfile(self, outfpath : str) -> MultiFast5File:
        # TODO: remove
        # return File(outfpath, 'w')
        return MultiFast5File(outfpath, mode='w')
    # end def
# end class
