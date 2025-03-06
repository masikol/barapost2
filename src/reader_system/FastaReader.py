
from src.containers.Fasta import Fasta
from src.util.prune_seq import prune_seq
from src.reader_system.FileReader import FileReader


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

        seq_record = Fasta(
            header=header[1:], # skip the first character
            seq=''.join(seq_lines)
        )
        if self.max_seq_len != -1:
            seq_record = prune_seq(seq_record, self.max_seq_len)
        # end if
        return seq_record
    # end def

    def _count_records_in_curr_file(self) -> int:
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
