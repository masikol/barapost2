import pytest

from src.containers.Fastq import Fastq


PHRED_OFFSET = 33

UNIFORM_Q = 7
UNIFORM_CHAR = chr(UNIFORM_Q + PHRED_OFFSET)


@pytest.fixture
def some_fastq_record() -> Fastq:
    random_seq = 'CATGATGCTAGC'
    return Fastq(
        header='some_seq',
        seq=random_seq,
        comment='+',
        quality=UNIFORM_CHAR * len(random_seq),
        phred_offset=PHRED_OFFSET
    )
# end def


@pytest.fixture
def char_for_Q10() -> str:
    return chr(10 + PHRED_OFFSET)
# end def

@pytest.fixture
def char_for_Q20() -> str:
    return chr(20 + PHRED_OFFSET)
# end def

@pytest.fixture
def char_for_Q30() -> str:
    return chr(30 + PHRED_OFFSET)
# end def



class TestFastq:

    def test_phred_char_to_pe(self,
                              some_fastq_record : Fastq,
                              char_for_Q10 : str,
                              char_for_Q20 : str,
                              char_for_Q30 : str):
        char_pe_zip = zip(
            (char_for_Q10, char_for_Q20, char_for_Q30),
            (1e-1, 1e-2, 1e-3)
        )
        for char, pe in char_pe_zip:
            diff = abs(
                some_fastq_record._phred_char_to_pe(char) - pe
            )
            assert diff < 1e-6
        # end def
    # end def

    def test_get_average_quality_uniform(self,
                                         some_fastq_record : Fastq):
        expected = float(UNIFORM_Q)
        observed = some_fastq_record.get_average_quality()
        diff = abs(expected - observed)
        assert diff < 1e-6
    # end def
# end def
