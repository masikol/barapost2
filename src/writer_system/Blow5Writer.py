
import os
import pyslow5 as s5

# TODO: remove
# from src.config.config import OUTPUT_DIR

from src.containers.Blow5 import Blow5

from src.writer_system.FileWriter import FileWriter

# TODO: S/BLOW5 is to be implemented later
class Blow5Writer(FileWriter):

    def _write_single_record(self,
                             sec_record : Blow5,
                             out_file_handle : s5.Open):
        from_record = sec_record.record
        to_record, to_aux = out_file_handle.get_empty_record(aux=True)

        to_record = {key : from_record[key] for key in to_record.keys()}
        to_aux    = {key : from_record[key] for key in    to_aux.keys()}

        out_file_handle.write_record(to_record, to_aux)
    # end def

    def _get_out_file_path(self, label : str, index : str) -> str:
        return os.path.join(
            self.outdir_path,
            f'{label}_{index}.{self.ext}'
        )
    # end def

    def _open_new_outfile(self, outfpath : str) -> s5.Open:
        return s5.Open(outfpath, 'w')
    # end def

# end class
