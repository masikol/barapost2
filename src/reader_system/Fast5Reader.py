
# TODO: remove
# from h5py import File
from ont_fast5_api.fast5_interface import get_fast5_file

from src.containers.Fast5 import Fast5
from src.reader_system.FileReader import FileReader
from src.util.simplify_read_id import simplify_read_id


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
        # TODO: remove
        # return Fast5(file_handle = self.reader, read_id = read_id)
        return Fast5(
            read_data=self.reader.get_read(read_id)
        )
    # end def

    # TODO: remove
    # def _detect_single_fast5(self):
    #     return 'Raw' in self.reader.keys()
    # # end def


    def open(self) -> None:
        # TODO: remove
        # self.reader = File(self._curr_file_path, 'r')
        # if self._detect_single_fast5():
        #     read_id = 'read_{}'.format(
        #         simplify_read_id(self.reader.filename) # read id is in the filename
        #     )
        #     self.reader_iterator = iter( (read_id,) )
        # else:
        #     self.reader_iterator = iter(self.reader)
        # # end if

        self.reader = get_fast5_file(self._curr_file_path, mode='r')
        self.reader_iterator = iter(self.reader.get_reads())
    # end def


    # TODO: Manualy close it after writing!!!
    def close(self) -> None: # Do not close FAST5 files till write it
        self.reader.close()
    # end def
# end class
