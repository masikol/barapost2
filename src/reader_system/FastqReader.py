
from src.reader_system.FileReader import FileReader
from src.containers.Fastq import Fastq


class FastqReader(FileReader):

    def _check_file_end(self, record : Fastq) -> bool:
        return record.header == ''
    # end def

    def _read_single_record(self) -> Fastq:
        header    = self.reader.readline().strip().lstrip('@')
        seq       = self.reader.readline().strip()
        plus_line = self.reader.readline().strip()
        quality   = self.reader.readline().strip()

        return Fastq(
            header=header,
            seq=seq,
            plus_line=plus_line,
            quality=quality
        )
    # end def
# end class
