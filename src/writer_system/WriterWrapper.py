
import logging

from src.writer_system.FileWriter  import FileWriter
from src.writer_system.FastaWriter import FastaWriter
from src.writer_system.FastqWriter import FastqWriter
from src.writer_system.Pod5Writer  import Pod5Writer
from src.writer_system.Fast5Writer import Fast5Writer
# TODO: S/BLOW5 is to be implemented later
# from src.writer_system.Blow5Writer import Blow5Writer
# from src.writer_system.Slow5Writer import Slow5Writer

# TODO: don't forget to move higher to some config abstraction level
logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)


class WriterWrapper(object):
    def __init__(self,
                 outdir_path : str,
                 _type_ : str,
                 _gzip_ : bool = False,
                 n_max_out : int = 4000,
                 line_width : int = 60):

        _type_ = _type_.lower()
        if _type_ == 'fasta':
            self.writer = FastaWriter(outdir_path, _gzip_, n_max_out, 'fasta', line_width)
        elif _type_ == 'fastq':
            self.writer = FastqWriter(outdir_path, _gzip_, n_max_out, 'fastq')
        elif _type_ == 'pod5':
            self.writer = Pod5Writer( outdir_path, False,  n_max_out,  'pod5')
        elif _type_ == 'fast5':
            self.writer = Fast5Writer(outdir_path, False,  n_max_out, 'fast5')
        # TODO: S/BLOW5 is to be implemented later
        # elif _type_ == 'blow5':
        #     self.writer = Blow5Writer(outdir_path, False,  n_max_out, 'blow5')
        # elif _type_ == 'slow5':
        #     self.writer = Slow5Writer(outdir_path, False,  n_max_out, 'slow5')
        else:
            raise ValueError(
                f'Invalid `_type_` argument: `{_type_}`. Allowed types: `fasta`, `fastq`, `pod5`, `fast5`.'
                # TODO: S/BLOW5 is to be implemented later
                # f'Invalid `_type_` argument: `{_type_}`. Allowed types: `fasta`, `fastq`, `pod5`, `fast5`, `blow5`, `slow5`.'
            )

        # end if
        
        # TODO: implement POD5, BLOW5, SLOW5 compression
        # See pod5 and pyslow5 packages
        # TODO: S/BLOW5 is to be implemented later
        # if _gzip_ and _type_.lower() in ('pod5', 'fast5', 'blow5', 'slow5'):
        if _gzip_ and _type_.lower() in ('pod5', 'fast5'):
            logger.warning(f'Cannot gzip {_type_} data. Ignoring output compression.')
        # end if
    # end def

    def __enter__(self) -> FileWriter:
        return self.writer
    # end def

    def __exit__(self, type, value, traceback):
        self.writer.close()
    # end def
# end class
