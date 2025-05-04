
from src.containers.Fasta import Fasta
from src.containers.Fastq import Fastq
from src.containers.SeqRecord import SeqRecord


def prune_seq(seq_record : SeqRecord,
              new_seq_len : int) -> SeqRecord:

    old_seq_len = len(seq_record.get_seq())
    if new_seq_len >= old_seq_len:
        return seq_record
    # end if

    # Make a copy so that seq_record doesn't get modified
    new_seq_record = seq_record.copy()

    if type(seq_record) == Fasta:
        new_seq_record.seq = _prune_string(seq_record.seq, new_seq_len)
    elif type(seq_record) == Fastq:
        new_seq_record.seq     = _prune_string(seq_record.seq, new_seq_len)
        new_seq_record.quality = _prune_string(seq_record.quality, new_seq_len)
    else:
        raise TypeError(
            'Invalid SeqRecord type: `{}`'.format(seq_record)
        )
    # end if
    return new_seq_record
# end def


def _prune_string(string: str, new_seq_len : int) -> str:
    old_len = len(string)
    flank_len = (old_len - new_seq_len) // 2
    return string[flank_len : (flank_len + new_seq_len)]
# end def
