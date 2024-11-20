
import os
from pyslow5 import Open

from src.config.config import OUTPUT_DIR

from src.containers.Slow5 import Slow5

from src.writer_system.FileWriter import FileWriter


class Slow5Writer(FileWriter):

    def _write_single_record(self,
                             sec_record : Slow5,
                             out_file_handle : Open):
        out_file_handle.write_record(sec_record.record)
    # end def

    def _get_out_file_path(self, label : str, index : str) -> str:
        return os.path.join(
            OUTPUT_DIR,
            f'{label}_{index}.{self.ext}'
        )
    # end def

    def _open_new_outfile(self, outfpath : str) -> Open:
        return Open(outfpath, 'w')
    # end def
# end class
