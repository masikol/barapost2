
import pytest

from src.config.hits import SEP
from src.containers.AlignResult import AlignResult
from src.containers.HitToDownload import HitToDownload


SOME_ACCESSION = 'CP045701.2'
SOME_RECORD_NAME = 'Pseudomonas brassicacearum strain S-1 chromosome, complete genome'


@pytest.fixture
def some_hit() -> HitToDownload:
    return HitToDownload(
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


class TestHitToDownload:

    def test_to_tsv_row(self, some_hit : HitToDownload):
        expected = SEP.join(
            (
                SOME_ACCESSION,
                SOME_RECORD_NAME,
                '2',
                '0'
            )
        ) + '\n'
        observed = some_hit.to_tsv_row()
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
        expected = HitToDownload(
            accession=SOME_ACCESSION,
            record_name=SOME_RECORD_NAME,
            hit_count=2,
            replicons_checked=False
        )
        observed = HitToDownload.from_tsv_row(some_tsv_row)
        assert observed == observed, str(observed) + '\n' + str(expected)
    # end def

    def test_increment_default(self, some_hit : HitToDownload):
        some_hit.hit_count = 5
        expected = some_hit.hit_count + 1

        some_hit.increment()
        observed = some_hit.hit_count

        assert observed == expected
    # end def

    def test_increment(self, some_hit : HitToDownload):
        some_hit.hit_count = 5
        increment_value = 4
        expected = some_hit.hit_count + increment_value

        some_hit.increment(increment_value)
        observed = some_hit.hit_count

        assert observed == expected
    # end def

    def test_from_align_result(self,
                               some_align_result : AlignResult):
        hit = HitToDownload.from_align_result(some_align_result)
        assert hit.accession   == SOME_ACCESSION
        assert hit.record_name == SOME_RECORD_NAME
        assert hit.hit_count == 1
        assert hit.replicons_checked == False
    # end def
# end class
