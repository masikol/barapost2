
from typing import TextIO

from src.containers.Fasta import Fasta
from src.writer_system.FileWriter import FileWriter


class FastaWriter(FileWriter):

    def _write_single_record(self,
                             sec_record : Fasta,
                             out_file_handle : TextIO):
        out_file_handle.write(f'>{sec_record.header}\n')
        out_file_handle.write(f'{sec_record.seq}\n')
    # end def
# end class

