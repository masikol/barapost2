
from typing import Sequence

from src.containers.Fastq import Fastq
from src.util.prune_seq import prune_seq
from src.reader_system.FileReader import FileReader


class FastqReader(FileReader):

    def __init__(self,
                 file_paths : Sequence[str],
                 packet_mode : str = 'seq_count',
                 packet_size : int = 1,
                 probing_batch_size : int = -1,
                 max_seq_len : int = -1,
                 n_first_skip_dict : dict = dict(),
                 phred_offset : int = 33):
        super().__init__(
            file_paths,
            packet_mode,
            packet_size,
            probing_batch_size,
            max_seq_len,
            n_first_skip_dict
        )
        self.phred_offset = phred_offset
    # end def

    def _check_file_end(self, record : Fastq) -> bool:
        return record.header == ''
    # end def

    def _read_single_record(self) -> Fastq:
        header    = self.reader.readline().strip()[1:] # skip the first character
        seq       = self.reader.readline().strip()
        comment   = self.reader.readline().strip()
        quality   = self.reader.readline().strip()

        seq_record = Fastq(
            header=header,
            seq=seq,
            comment=comment,
            quality=quality,
            phred_offset=self.phred_offset
        )

        if self.max_seq_len != -1:
            seq_record = prune_seq(seq_record, self.max_seq_len)
        # end if

        return seq_record
    # end def

    def _count_records_in_curr_file(self) -> int:
        with self._open_gzipwise(self._curr_file_path) as input_handle:
            line_count = sum(
                (
                    1 for line in input_handle.readlines()
                )
            )
        # end with
        return line_count // 4
    # end def
# end class
