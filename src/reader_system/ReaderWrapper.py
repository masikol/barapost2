
import os
import logging
from typing import Generator, Sequence, MutableSequence

import src.filesystem as fs
from src.containers.SeqRecord import SeqRecord

from src.reader_system.FileReader  import FileReader
from src.reader_system.FastaReader import FastaReader
from src.reader_system.FastqReader import FastqReader
from src.reader_system.Fast5Reader import Fast5Reader
from src.reader_system.Pod5Reader  import Pod5Reader
# TODO: S/BLOW5 is to be implemented later
# from src.reader_system.Slow5Reader import Slow5Reader
# from src.reader_system.Blow5Reader import Blow5Reader


# TODO: don't forget to move higher to some config abstraction level
logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)


class ReaderWrapper(object):

    def __init__(self,
                 file_paths : Sequence[str],
                 packet_mode : str = 'seq_count',
                 packet_size : int = 1,
                 probing_batch_size : int = -1,
                 max_seq_len : int = -1,
                 n_first_skip_dict : dict = dict()):

        # TODO: we'll handle this at the arg parsing stage
        # if not os.path.isfile(file_path):
        #     raise FileNotFoundError(
        #         f'File `{file_path}` does not exist.'
        #     )
        # # end if

        # TODO: do we really need to assign these vars to self. fields?
        # They are used in the __init__ only
        self.file_paths         = file_paths
        self.packet_mode        = packet_mode
        self.packet_size        = packet_size
        self.probing_batch_size = probing_batch_size
        self.max_seq_len        = max_seq_len

        self._validate_positive_integer(self.packet_size, 'packet_size')
        self._validate_positive_integer(
            self.probing_batch_size,
            'probing_batch_size',
            allow_minus_one = True
        )
        self._validate_positive_integer(
            self.max_seq_len,
            'max_seq_len',
            allow_minus_one = True
        )

        if self.packet_mode == 'seq_count' and self.max_seq_len != -1:
            logger.warning(
                f'The `max_seq_len` parameter is avalible only in `sum_seq_len` mode.'
            )
            logger.warning('Ignoring the `max_seq_len` parameter.')
            self.max_seq_len = -1
        # end if

        if self.packet_mode not in ('seq_count', 'sum_seq_len'):
            logger.warning(f'Invalid mode: `{self.packet_mode}`. Setting mode to `seq_count`.')
            self.packet_mode = 'seq_count'
        # end if

        # TODO:
        # 1. catch StopIteration? Or we will handle this at the arg parsing stage?
        # 2. We will assume that file_paths is homogenous: only fasta, only fastq as so on
        curr_file_path = next(iter(file_paths))

        if fs.is_fasta(curr_file_path):
            self.reader = FastaReader(
                file_paths=self.file_paths,
                packet_mode=self.packet_mode,
                packet_size=self.packet_size,
                probing_batch_size=self.probing_batch_size,
                max_seq_len=self.max_seq_len,
                n_first_skip_dict=n_first_skip_dict
            )
        elif fs.is_fastq(curr_file_path):
            self.reader = FastqReader(
                file_paths=self.file_paths,
                packet_mode=self.packet_mode,
                packet_size=self.packet_size,
                probing_batch_size=self.probing_batch_size,
                max_seq_len=self.max_seq_len,
                n_first_skip_dict=n_first_skip_dict
            )
        elif fs.is_fast5(curr_file_path):
            self.reader = Fast5Reader(
                file_paths=self.file_paths,
                n_first_skip_dict=n_first_skip_dict
            )
        elif fs.is_pod5(curr_file_path):
            self.reader = Pod5Reader(
                file_paths=self.file_paths,
                n_first_skip_dict=n_first_skip_dict
            )
        # TODO: S/BLOW5 is to be implemented later
        # elif fs.is_blow5(curr_file_path):
        #     self.reader = Blow5Reader(
        #         file_paths=self.file_paths,
        #         n_first_skip_dict=n_first_skip_dict
        #     )
        # elif fs.is_slow5(curr_file_path):
        #     self.reader = Slow5Reader(
        #         file_paths=self.file_paths,
        #         n_first_skip_dict=n_first_skip_dict
        #     )
        else:
            err_msg = self._make_invalid_file_type_err_msg(curr_file_path)
            raise ValueError(err_msg)
        # end if
    # end def

    def _validate_positive_integer(self,
                                   value : int,
                                   name : str,
                                   allow_minus_one : bool = False):
        if value < 0 and not (allow_minus_one and value == -1):
            raise ValueError(f'`{name}` must be a positive integer. Received `{name}`=`{value}`')
        # end if
    # end def

    def _make_invalid_file_type_err_msg(self, file_path : str):
        file_type = fs.get_hts_file_type(file_path)
        allowed_extensions = fs.FASTA_EXTENSIONS \
                           | fs.FASTQ_EXTENSIONS \
                           | {'fast5', 'pod5'}
                           # TODO: S/BLOW5 is to be implemented later
                           # | {'fast5', 'pod5', 'blow5', 'slow5'}
        return 'Invalid file type (extension): `{}`. Allowed types: {}.'.format(
            file_type,
            ', '.join(allowed_extensions)
        )
    # end def

    def __next__(self) -> Generator[MutableSequence[SeqRecord], None, None]:
        return next(self.reader)
    # end def

    def __enter__(self) -> FileReader:
        self.reader.open()
        return self.reader
    # end def

    def __exit__(self, type, value, traceback):
        self.reader.close()
    # end def
# end class
