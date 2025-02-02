
from pod5 import DatasetReader

from src.reader_system.FileReader import FileReader
from src.containers.Pod5 import Pod5


class Pod5Reader(FileReader):

    def _check_file_end(self, record : Pod5) -> bool:
        return False
    # end def

    def _read_single_record(self) -> Pod5:
        try:
            record = next(self.reader_generator)
        except StopIteration:
            raise
        # end try
        return Pod5(record = record)
    # end def

    def open(self) -> None:
        with DatasetReader(self._curr_file_path) as file:
            self.reader = file
            self.reader_generator = self.reader.reads()
        # end with
    # end def

    def close(self) -> None:
        pass
    # end def
# end class
