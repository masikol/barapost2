
from ont_fast5_api.fast5_interface import get_fast5_file

from src.containers.Fast5 import Fast5
from src.reader_system.FileReader import FileReader


class Fast5Reader(FileReader):

    def _check_file_end(self, record : Fast5) -> bool:
        return False
    # end def


    def _read_single_record(self) -> Fast5:
        # TODO: is this really more effective than
        #   just iterating over get_reads()?
        try:
            read_id = next(self.reader_iterator).read_id
        except StopIteration:
            raise
        # end try
        return Fast5(
            record=self.reader.get_read(read_id)
        )
    # end def


    def open(self) -> None:
        self.reader = get_fast5_file(self._curr_file_path, mode='r')
        self.reader_iterator = iter(self.reader.get_reads())
    # end def


    # TODO: Manualy close it after writing!!!
    def close(self) -> None: # Do not close FAST5 files till write it
        self.reader.close()
    # end def

    def _count_records_in_curr_file(self) -> int:
        f5 = get_fast5_file(self._curr_file_path, mode='r')
        return len(f5.get_read_ids())
    # end def
# end class
