
from src.containers.Fasta import Fasta
from src.containers.Fastq import Fastq
from src.containers.RealSeqRecord import RealSeqRecord


# TODO: test
def prune_seq(seq_record : RealSeqRecord,
              new_seq_len : int) -> RealSeqRecord:
    # TODO: seq_record gets modified it!

    old_seq_len = len(seq_record.get_seq())
    if new_seq_len >= old_seq_len:
        return seq_record
    # end if

    if type(seq_record) == Fasta:
        seq_record.seq = _prune_string(seq_record.seq, new_seq_len)
    elif type(seq_record) == Fastq:
        seq_record.seq     = _prune_string(seq_record.seq, new_seq_len)
        seq_record.quality = _prune_string(seq_record.quality, new_seq_len)
    else:
        raise TypeError(
            'Invalid RealSeqRecord type: `{}`'.format(seq_record)
        )
    # end if
    return seq_record
# end def

# TODO: test? it's 'private'.
def _prune_string(string: str, new_seq_len : int) -> str:
    old_len = len(string)
    flank_len = (old_len - new_seq_len) // 2
    return string[flank_len : (flank_len + new_seq_len)]
# end def
