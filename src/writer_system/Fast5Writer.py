
import os
import re
import logging

from ont_fast5_api.multi_fast5 import MultiFast5File

from src.containers.Fast5 import Fast5
from src.writer_system.FileWriter import FileWriter


class Fast5Writer(FileWriter):

    def _write_single_record(self,
                             seq_record : Fast5,
                             out_file_handle : MultiFast5File):
        out_file_handle.add_existing_read(seq_record.read_data)
    # end def

    def _get_out_file_path(self, label : str, index : str) -> str:
        return os.path.join(
            self.outdir_path,
            f'{label}_{index}.{self.ext}'
        )
    # end def

    def _open_new_outfile(self, outfpath : str) -> MultiFast5File:
        return MultiFast5File(outfpath, mode='w')
    # end def
# end class
