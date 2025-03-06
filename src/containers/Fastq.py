
import math
import logging
import statistics
from functools import partial
from typing import Sequence, TypeAlias

from src.containers.SeqRecord import SeqRecord


SeqPacket : TypeAlias = Sequence[SeqRecord]


logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)


class Fastq(SeqRecord):

    __slots__ = (
        'header',
        'seq',
        'comment',
        'quality',
        'phred_offset',
        'average_quality',
    )

    def __init__(self,
                 header : str,
                 seq : str,
                 comment : str,
                 quality : str,
                 phred_offset : int = 33):
        self.header = header
        self.seq = seq
        self.comment = comment
        self.quality = quality
        self.phred_offset = phred_offset # arg parsing ensures that phred_offset is valid
        self._average_quality = None
    # end def

    def get_average_quality(self) -> float:
        if self._average_quality is None:
            self._average_quality = self._calc_average_quality()
        # end def
        return self._average_quality
    # end def

    def _calc_average_quality(self) -> float:
        avg_error_prob = statistics.mean(
            map(self._phred_char_to_pe, self.quality)
        )
        return round(
            pe_to_Q(avg_error_prob),
            2
        )
    # end def

    def _phred_char_to_pe(self, char : str) -> float:
        # pe is error probability
        Q = ord(char) - self.phred_offset
        return Q_to_pe(Q)
    # end def

    def __str__(self):
        seq_concise     = self._get_consice_str(self.seq)
        quality_concise = self._get_consice_str(self.quality)
        return f'''header: {self.header},
seq: {seq_concise},
comment: {self.comment},
quality: {quality_concise}.\n'''
    # end def

    def __repr__(self):
        seq_concise     = self._get_consice_str(self.seq)
        quality_concise = self._get_consice_str(self.quality)
        return f'''Fastq(
    header={self.header!r}, 
    sequence={seq_concise!r}, 
    comment={self.comment!r}, 
    quality={quality_concise!r}
)'''
    # end def

    def _get_consice_str(self, string):
        n_chars_show = 30
        if len(self.seq) <= n_chars_show*2:
            return self.seq
        # end if
        n_chars_omitted = len(self.seq) - 2*n_chars_show
        return '{}../{:,}chars/..{}'.format(
            string[:n_chars_show],
            n_chars_omitted,
            string[-n_chars_show:]
        )
    # end def

    def get_seq_id(self) -> str:
        return self.header.partition(' ')[0]
    # end def
# end class


def Q_to_pe(Q : float) -> float:
    return 10.0 ** (-Q / 10.0)
# end def


def pe_to_Q(error_prob : float):
    return -10.0 * math.log10(error_prob)
# end def


def make_quality_dict(packet : SeqPacket) -> dict[str, float]:
    packet_type = type(
        next(iter(packet))
    )
    if packet_type == Fastq:
        return {
            sr.get_seq_id() : sr.get_average_quality()
                for sr in packet
        }
    # end if
    return {
        sr.get_seq_id() : None for sr in packet
    }
# end def
