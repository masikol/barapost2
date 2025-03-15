import pytest

import math

from src.containers.Fastq import Fastq, Q_to_pe, pe_to_Q, make_quality_dict

PHRED_OFFSET = 33

UNIFORM_Q = 7
UNIFORM_CHAR = chr(UNIFORM_Q + PHRED_OFFSET)


@pytest.fixture
def some_fastq_record() -> Fastq:
    random_seq = 'CATGATGCTAGC'
    return Fastq(
        header = 'some_seq',
        seq = random_seq,
        comment = '+',
        quality = UNIFORM_CHAR * len(random_seq),
        phred_offset = PHRED_OFFSET
    )
# end def

class DummyRecord:
    def __init__(self, seq_id: str) -> None:
        self._seq_id: str = seq_id
    # end def

    def get_seq_id(self) -> str:
        return self._seq_id
    # end def
# end class

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


# get_average_quality test
def test_get_average_quality_uniform(some_fastq_record: Fastq) -> None:
    expected: float = float(UNIFORM_Q)
    observed: float = some_fastq_record.get_average_quality()
    assert abs(expected - observed) < 1e-6
# end def

def test_get_average_quality_non_uniform() -> None:
    quality_string: str = chr(10 + PHRED_OFFSET) + chr(20 + PHRED_OFFSET) + chr(30 + PHRED_OFFSET)
    record: Fastq = Fastq(
        header = 'non_uniform_seq',
        seq = 'ATC',
        comment = '+',
        quality = quality_string,
        phred_offset = PHRED_OFFSET
    )
    avg_error: float = (0.1 + 0.01 + 0.001) / 3
    expected: float = round(-10 * math.log10(avg_error), 2)
    observed: float = record.get_average_quality()
    assert abs(expected - observed) < 1e-6
# end def

# Q_to_pe test
def test_Q_to_pe() -> None:
    assert abs(Q_to_pe(10) - 0.1) < 1e-6
    assert abs(Q_to_pe(20) - 0.01) < 1e-6
    assert abs(Q_to_pe(30) - 0.001) < 1e-6
# end def

# pe_to_Q test
def test_pe_to_Q() -> None:
    assert abs(pe_to_Q(0.1) - 10) < 1e-6
    assert abs(pe_to_Q(0.01) - 20) < 1e-6
    assert abs(pe_to_Q(0.001) - 30) < 1e-6
# end def

def test_pe_to_Q_invalid_zero() -> None:
    with pytest.raises(ValueError):
        pe_to_Q(0.0)
    # end with
# end def

def test_pe_to_Q_invalid_negative() -> None:
    with pytest.raises(ValueError):
        pe_to_Q(-0.1)
    # end with
# end def

# make_quality_dict tests
def test_make_quality_dict_with_fastq(some_fastq_record: Fastq) -> None:
    record1: Fastq = some_fastq_record
    record2: Fastq = Fastq(
        header = 'seq2 extra',
        seq = 'GCTA',
        comment = '+',
        quality = chr(20 + PHRED_OFFSET) * 4,
        phred_offset = PHRED_OFFSET
    )
    packet: list[Fastq] = [record1, record2]
    result: dict[str, float] = make_quality_dict(packet)
    expected1: float = record1.get_average_quality()
    expected2: float = record2.get_average_quality()
    assert 'some_seq' in result
    assert 'seq2' in result
    assert abs(result['some_seq'] - expected1) < 1e-6
    assert abs(result['seq2'] - expected2) < 1e-6
# end def

def test_make_quality_dict_with_dummy_records() -> None:
    dummy1 = DummyRecord('dummy1')
    dummy2 = DummyRecord('dummy2')
    packet: list = [dummy1, dummy2]
    result: dict[str, None] = make_quality_dict(packet)
    assert result == {'dummy1': None, 'dummy2': None}
# end def

def test_make_quality_dict_empty() -> None:
    with pytest.raises(StopIteration):
        make_quality_dict([])
    # end with
# end def
