
import pytest

from src.config.seq_db import SEP
from src.containers.AlignResult import AlignResult
from src.containers.SeqDbListRecord import SeqDbListRecord


SOME_ACCESSION = 'CP045701.2'
SOME_RECORD_NAME = 'Pseudomonas brassicacearum strain S-1 chromosome, complete genome'


@pytest.fixture
def some_record() -> SeqDbListRecord:
    return SeqDbListRecord(
        accession=SOME_ACCESSION,
        record_name=SOME_RECORD_NAME,
        hit_count=2,
        replicons_checked=False
    )
# end def

@pytest.fixture
def some_align_result() -> AlignResult:
    return AlignResult(
        query_id='query_seq',
        hit_name=SOME_RECORD_NAME,
        hit_accession=SOME_ACCESSION,
        query_length=1000,
        alignment_length=1000,
        identity=999,
        gaps=0,
        evalue=0.0,
        avg_quality=6.8,
        accuracy=98.7
    )
# end def


class TestSeqDbListRecord:

    def test_to_tsv_row(self, some_record : SeqDbListRecord):
        expected = SEP.join(
            (
                SOME_ACCESSION,
                SOME_RECORD_NAME,
                '2',
                '0'
            )
        ) + '\n'
        observed = some_record.to_tsv_row()
        assert observed == expected
    # end def


    def test_from_tsv_row(self):
        some_tsv_row = SEP.join(
            (
                SOME_ACCESSION,
                SOME_RECORD_NAME,
                '2',
                '0'
            )
        ) + '\n'
        expected = SeqDbListRecord(
            accession=SOME_ACCESSION,
            record_name=SOME_RECORD_NAME,
            hit_count=2,
            replicons_checked=False
        )
        observed = SeqDbListRecord.from_tsv_row(some_tsv_row)
        assert observed == observed, str(observed) + '\n' + str(expected)
    # end def

    def test_increment_default(self, some_record : SeqDbListRecord):
        some_record.hit_count = 5
        expected = some_record.hit_count + 1

        some_record.increment()
        observed = some_record.hit_count

        assert observed == expected
    # end def

    def test_increment(self, some_record : SeqDbListRecord):
        some_record.hit_count = 5
        increment_value = 4
        expected = some_record.hit_count + increment_value

        some_record.increment(increment_value)
        observed = some_record.hit_count

        assert observed == expected
    # end def

    def test_from_align_result(self,
                               some_align_result : AlignResult):
        record = SeqDbListRecord.from_align_result(some_align_result)
        assert record.accession   == SOME_ACCESSION
        assert record.record_name == SOME_RECORD_NAME
        assert record.hit_count == 1
        assert record.replicons_checked == False
    # end def
# end class
