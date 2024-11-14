
import pytest

from src.network.RequestFailError import RequestFailError
from src.network.insistent_https_get import insistent_https_get


# === Fixtures ===

@pytest.fixture
def correct_params() -> dict:
    return {
        'server'          : 'ncbi.nlm.nih.gov',
        'url'             : '/nuccore/CP045701.2',
        'request_for'     : 'P. brassicacearum S-1 GenBank page',
        'accession_number': 'CP045701.2',
        'timeout'         : 30,
    }
# end def

@pytest.fixture
def incorrect_params1() -> dict:
    return {
        'server'          : 'ncbiERROR.nlm.nih.gov',
        'url'             : '/nuccore/CP045701.2',
        'request_for'     : 'P. brassicacearum S-1 GenBank page',
        'accession_number': 'CP045701.2',
        'timeout'         : 30,
    }
# end def


@pytest.fixture
def incorrect_params2() -> dict:
    return {
        'server'          : 'ncbi.nlm.nih.gov',
        'url'             : '/nuccoreERROR/CP045701.2',
        'request_for'     : 'P. brassicacearum S-1 GenBank page',
        'accession_number': 'CP045701.2',
        'timeout'         : 30,
    }
# end def


# === Test classes ===

class TestInsistentHttpsGet:
    # Class for testing `src.network.insistent_https_get`

    def test_correct_params(self, correct_params: dict):
        try:
            insistent_https_get(
                correct_params['server'],
                correct_params['url'],
                correct_params['request_for'],
                correct_params['accession_number'],
                correct_params['timeout'],
            )
        except RequestFailError as err:
            err_msg = '`insistent_https_get` raised an exception {}'.format(err)
            assert False, err_msg
    # end def


    def test_incorrect_params1(self, incorrect_params1: dict):
        with pytest.raises(RequestFailError):
            insistent_https_get(
                incorrect_params1['server'],
                incorrect_params1['url'],
                incorrect_params1['request_for'],
                incorrect_params1['accession_number'],
                incorrect_params1['timeout'],
            )
        # end with
    # end def

    def test_incorrect_params2(self, incorrect_params2: dict):
        with pytest.raises(RequestFailError):
            insistent_https_get(
                incorrect_params2['server'],
                incorrect_params2['url'],
                incorrect_params2['request_for'],
                incorrect_params2['accession_number'],
                incorrect_params2['timeout'],
            )
        # end with
    # end def
# end class
