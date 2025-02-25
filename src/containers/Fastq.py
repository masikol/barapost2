
import math
import logging
import statistics
from typing import Sequence, TypeAlias

from src.containers.RealSeqRecord import RealSeqRecord


SeqPacket : TypeAlias = Sequence[RealSeqRecord]


logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)


class Fastq(RealSeqRecord):

    __slots__ = ('header', 'seq', 'plus_line', 'quality', 'offset')

    def __init__(self,
                 header : str,
                 seq : str,
                 plus_line : str,
                 quality : str,
                 offset : int = 33):
        self.header = header
        self.seq = seq
        self.plus_line = plus_line
        self.quality = quality

        if offset not in (33, 64):
            logger.warning(f'Unexpected offset: `{offset}`. Setting offset to 33.')
            self.offset = 33
        else:
            self.offset = offset
        # end if
    # end def

    def average_quality(self) -> float:
        # TODO: use phred offset here!!!
        avg_error_prob = statistics.mean(
            map(phred_char_to_pe, self.quality)
        )
        return round(
            pe_to_Q(avg_error_prob),
            2
        )
    # end def

    def __str__(self):
        seq_concise     = self._get_consice_str(self.seq)
        quality_concise = self._get_consice_str(self.quality)
        return f'''header: {self.header},
seq: {seq_concise},
plus_line: {self.plus_line},
quality: {quality_concise}.\n'''
    # end def

    def __repr__(self):
        seq_concise     = self._get_consice_str(self.seq)
        quality_concise = self._get_consice_str(self.quality)
        return f'''Fastq(
    header={self.header!r}, 
    sequence={seq_concise!r}, 
    plus_line={self.plus_line!r}, 
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

    # TODO: test
    def get_seq_id(self) -> str:
        return self.header.partition(' ')[0]
    # end def
# end class


def phred_char_to_pe(char : str, offset : int = 33) -> float:
    # pe is error probability
    Q = ord(char) - offset
    return Q_to_pe(Q)
# end def


def Q_to_pe(Q : float) -> float:
    return 10 ** (-Q / 10)
# end def


def pe_to_Q(error_prob : float):
    return -10 * math.log10(error_prob)
# end def


def make_quality_dict(packet : SeqPacket) -> dict[str, float]:
    packet_type = type(
        next(iter(packet))
    )
    if packet_type == Fastq:
        return {
            sr.get_seq_id() : sr.average_quality()
                for sr in packet
        }
    # end if
    return {
        sr.get_seq_id() : None for sr in packet
    }
# end def
