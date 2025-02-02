
from typing import TextIO

from src.containers.Fasta import Fasta
from src.writer_system.FileWriter import FileWriter


class FastaWriter(FileWriter):

    def __init__(self,
                 outdir_path: str,
                 _gzip_: bool,
                 n_max_out: int,
                 ext : str,
                 line_width : int):
        super().__init__(
            outdir_path,
            _gzip_,
            n_max_out,
            ext
        )
        self.line_width = line_width
    # end def

    def _write_single_record(self,
                             sec_record : Fasta,
                             out_file_handle : TextIO):
        out_file_handle.write(f'>{sec_record.header}\n')
        if self.line_width == 0: # validation must be done while argument parsing
            seq = sec_record.seq
        else:
            seq = self._split_seq_into_lines(sec_record.seq)
        # end if
        out_file_handle.write(f'{seq}\n')
    # end def

    def _split_seq_into_lines(self, seq : str) -> str:
        seq_len, line_width = len(seq), self.line_width
        n_lines = seq_len // self.line_width
        if seq_len % self.line_width != 0:
            n_lines += 1
        # end if
        lines = [None] * n_lines
        start = 0
        for i in range(n_lines):
            lines[i] = seq[start : start + line_width]
            start += line_width
        # end for
        return '\n'.join(lines)
    # end def
# end class
