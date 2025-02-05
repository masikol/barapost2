
import os
import gzip
from io import TextIOWrapper
from abc import ABC, abstractmethod
from typing import Generator, Callable, Sequence, MutableSequence

import src.filesystem as fs
from src.containers.SeqRecord import SeqRecord


class FileReader(ABC):

    def __init__(self,
                 file_paths : Sequence[str],
                 packet_mode : str = 'seq_count',
                 packet_size : int = 1,
                 probing_batch_size : int = -1,
                 max_seq_len : int = -1,
                 n_first_skip_dict : dict = dict()):

        self.file_paths = file_paths
        # TODO: catch StopIteration
        # Or we will handle this at the arg parsing stage?
        self._curr_file_path = next(iter(file_paths))
        self._curr_file_i = 0

        self.packet_size = packet_size
        self.probing_batch_size = probing_batch_size
        self.packet_mode = packet_mode
        self.max_seq_len = max_seq_len
        self.n_first_skip_dict = n_first_skip_dict # in_file_basename : n_records_to_skip

        self._packet = []
        self._sum_seq_len_read = 0
        self._n_records_read_total = 0
        self._end_of_curr_file = False

        if self.packet_mode == 'seq_count':
            self._make_packet = self._make_seq_count_packet
        elif self.packet_mode == 'sum_seq_len':
            self._make_packet = self._make_sum_seq_len_packet
        else:
            raise ValueError(
                f'Indalid packet_mode: `{self.packet_mode}`. Allowed modes: `seq_count`, `sum_seq_len`.'
            )
        # end if

        if max_seq_len == -1:
            self._increment_sum = lambda seq : len(seq)
        elif max_seq_len > 0:
            self._increment_sum = lambda seq : min(self.max_seq_len, len(seq))
        else:
            # TODO: this won't work is str (or sth, not int/float) is passed as max_seq_len
            # Anyway, this validation will be done at the arg parsing stage
            raise ValueError(
                f'Indalid max_seq_len: `{max_seq_len}`. It must be a positive integer or -1.'
            )
        # end if
    # end def

    @abstractmethod
    def _read_single_record(self) -> SeqRecord:
        raise NotImplementedError()
    # end def

    @abstractmethod
    def _check_file_end(self, record : SeqRecord) -> bool:
        raise NotImplementedError()
    # end def

    def _make_conditional_packet(self,
                                 condition : Callable) -> MutableSequence[SeqRecord]:

        while condition():
            record = self._read_single_record()

            if self._check_file_end(record):
                self._end_of_curr_file = True
                if len(self._packet) == 0:
                    self._reset_packet() # TODO: do we really need it here?
                    raise StopIteration
                else:
                    packet = self._packet
                    self._reset_packet()
                    return packet
                # end if
            # end if
            self._packet.append(record)

            if self.packet_mode == 'sum_seq_len':
                self._sum_seq_len_read += self._increment_sum(record.seq)
            # end if

            self._n_records_read_total += 1
        # end while

        packet = self._packet
        self._reset_packet()

        return packet
    # end def

    def _reset_packet(self):
        self._packet = []
        self._sum_seq_len_read = 0
    # end def


    def _make_seq_count_packet(self) -> MutableSequence[SeqRecord]:
        return self._make_conditional_packet(
            condition=self._seq_count_stop_condition
        )
    # end def

    def _make_sum_seq_len_packet(self) -> MutableSequence[SeqRecord]:
        return self._make_conditional_packet(
            condition=self._sum_seq_len_stop_condition
        )
    # end def

    def _seq_count_stop_condition(self) -> bool:
        return len(self._packet) < self.packet_size \
               and self._common_stop_condition()
    # end def

    def _sum_seq_len_stop_condition(self) -> bool:
        return self._sum_seq_len_read < self.packet_size \
               and self._common_stop_condition()
    # end def

    def _common_stop_condition(self) -> bool:
        return self.probing_batch_size == -1 \
               or self._n_records_read_total < self.probing_batch_size
    # end def


    # TODO: add return type hint
    def __iter__(self):
        return self
    # end def

    def __next__(self) -> Generator[MutableSequence[SeqRecord], None, None]:
        stop = self.probing_batch_size != -1 \
               and self._n_records_read_total >= self.probing_batch_size
        if stop:
            raise StopIteration
        # end if

        if self._end_of_curr_file:
            self._switch_to_next_input_file()
            self._end_of_curr_file = False
        # end if

        try:
            packet = self._make_packet()
        except StopIteration:
            # This will be raised if the previous packet exhausts an input file
            self._switch_to_next_input_file()
            self._end_of_curr_file = False
            packet = self._make_packet()
        # end try
        return packet
    # end def

    def _switch_to_next_input_file(self):
        # TODO: this won't work if self.file_paths is a generator
        #   It won't be a generator, anyway, so let it be so
        self._increment_curr_file_i()

        found = False
        while not found:
            self._curr_file_path = self.file_paths[self._curr_file_i]
            self.reader = self._open_gzipwise(self._curr_file_path)
            try:
                self._skip_n_first_records()
            except StopIteration:
                self._increment_curr_file_i()
            else:
                found = True
            # end try
        # end while
    # end def

    def _increment_curr_file_i(self):
        self._curr_file_i += 1
        if self._curr_file_i >= len(self.file_paths):
            raise StopIteration
        # end if
    # end def

    def open(self) -> None:
        self.reader = self._open_gzipwise(self._curr_file_path)
        self._skip_n_first_records()
    # end def

    def _open_gzipwise(self, infile_path : str) -> TextIOWrapper:
        if fs.is_gzipped(infile_path):
            return gzip.open(infile_path, mode='rt')
        else:
            return open(infile_path, mode='rt')
        # end if
    # end def

    def _skip_n_first_records(self):
        # TODO: set self.__end_of_curr_file here, not near _switch_to_next_input_file call!
        n_records_to_skip = self._get_n_records_to_skip()
        if n_records_to_skip > 0:
            record = None
            for i in range(n_records_to_skip):
                record = self._read_single_record()
            # end for
            if self._check_file_end(record):
                raise StopIteration
            # end if
        # end if
    # end def

    def _get_n_records_to_skip(self) -> int:
        # TODO: basename? really? COLLISION ALERT!
        in_file_basename = os.path.basename(self._curr_file_path)
        if not in_file_basename in self.n_first_skip_dict:
            return 0
        # end if
        # TODO: catch ValueError: conversion to int
        return self.n_first_skip_dict[in_file_basename]
    # end def

    def close(self) -> None:
        if self.reader:
            self.reader.close()
        # end if
    # end def
# end class
