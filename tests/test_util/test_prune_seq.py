
import pytest

from src.containers.Fasta import Fasta
from src.containers.Fastq import Fastq
from src.util.prune_seq import prune_seq


RANDOM_HEADER = 'pretty_woman'
RANDOM_SEQ    = 'CATGATGCTAGC'
SEQ_LEN = len(RANDOM_SEQ)


@pytest.fixture
def some_fasta_record() -> Fasta:
    return Fasta(
        header=RANDOM_HEADER,
        seq=RANDOM_SEQ
    )
# end def

# TODO: test fastq


class TestPruneSeqs:

    def test_prune_seq_longer(self, some_fasta_record : Fasta):
        # Tests src.util.prune_seq.prune_seq
        #   with new_seq_len larger than the length of seq_record.seq

        old_seq_len = len(some_fasta_record.get_seq())
        new_seq_len = old_seq_len + 3

        expected = old_seq_len
        observed = len(
            prune_seq(some_fasta_record, new_seq_len).get_seq()
        )

        assert observed == expected
    # end def

    def test_prune_seq_equal(self, some_fasta_record : Fasta):
        # Tests src.util.prune_seq.prune_seq
        #   with new_seq_len equals the length of seq_record.seq

        old_seq_len = len(some_fasta_record.get_seq())
        new_seq_len = old_seq_len

        expected = old_seq_len
        observed = len(
            prune_seq(some_fasta_record, new_seq_len).get_seq()
        )

        assert observed == expected
    # end def


    def test_prune_seq_shorter(self, some_fasta_record : Fasta):
        # Tests src.util.prune_seq.prune_seq
        #   with new_seq_len smaller than the length of seq_record.seq

        old_seq_len = len(some_fasta_record.get_seq())
        new_seq_len = old_seq_len - 3

        expected = new_seq_len
        observed = len(
            prune_seq(some_fasta_record, new_seq_len).get_seq()
        )

        assert observed == expected
    # end def

# end class
