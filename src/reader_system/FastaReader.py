
from src.reader_system.FileReader import FileReader
from src.containers.Fasta import Fasta


class FastaReader(FileReader):

    def _check_file_end(self, record : Fasta) -> bool:
        return record.header == ''
    # end def

    def _read_single_record(self) -> Fasta:
        header = self.reader.readline().strip()
        seq_lines = []

        while True:
            pos = self.reader.tell()
            line = self.reader.readline().strip()
            if line == '':
                break
            # end if
            if line.startswith('>'):
                self.reader.seek(pos)
                break
            # end if
            seq_lines.append(line)
        # end while

        seq = ''.join(seq_lines)
        return Fasta(
            header=header.lstrip('>'),
            seq=seq
        )
    # end def

    def _count_records_in_curr_file(self) -> bool:
        with self._open_gzipwise(self._curr_file_path) as input_handle:
            record_count = sum(
                (
                    1 if line.startswith('>') else 0
                    for line in input_handle.readlines()
                )
            )
        # end with
        return record_count
    # end def
# end class
