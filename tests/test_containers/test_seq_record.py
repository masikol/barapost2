
import pytest

from src.containers.Fasta import Fasta
from src.containers.Fastq import Fastq

RANDOM_SEQ = 'CATGATGCTAGC'


@pytest.fixture
def some_fasta_record() -> Fasta:
    return Fasta(
        header='some_seq',
        seq=RANDOM_SEQ
    )
# end def

@pytest.fixture
def some_fastq_record() -> Fastq:
    return Fastq(
        header='some_seq',
        seq=RANDOM_SEQ,
        comment='+',
        quality='7' * len(RANDOM_SEQ)
    )
# end def


class TestHTSRecord:

    def test_get_seq_fasta(self, some_fasta_record : Fasta):
        assert some_fasta_record.get_seq() == RANDOM_SEQ
    # end def

    def test_get_seq_fastq(self, some_fastq_record : Fastq):
        assert some_fastq_record.get_seq() == RANDOM_SEQ
    # end def
# end class
