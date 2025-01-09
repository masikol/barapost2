
import pytest

from src.network.insistent_https import insistent_https
from src.network.RequestFailError import RequestFailError


# === Fixtures ===

@pytest.fixture
def correct_params() -> dict:
    return {
        'server'          : 'ncbi.nlm.nih.gov',
        'server_path'     : '/nuccore/CP045701.2',
    }
# end def

@pytest.fixture
def correct_params_with_args() -> dict:
    return {
        'server'          : 'ncbi.nlm.nih.gov',
        'server_path'     : '/nuccore/CP045701.2',
        'args'            : {'report': 'gilist', 'format': 'text'},
    }
# end def

@pytest.fixture
def incorrect_params1() -> dict:
    return {
        'server'          : 'ncbiERROR.nlm.nih.gov',
        'server_path'     : '/nuccore/CP045701.2',
    }
# end def


@pytest.fixture
def incorrect_params2() -> dict:
    return {
        'server'          : 'ncbi.nlm.nih.gov',
        'server_path'     : '/nuccoreERROR/CP045701.2',
    }
# end def


# === Test classes ===

class TestInsistentHttpsGet:
    # Class for testing `src.network.insistent_https`

    def test_correct_params(self, correct_params: dict):
        try:
            insistent_https(
                server=correct_params['server'],
                server_path=correct_params['server_path'],
            )
        except RequestFailError as err:
            err_msg = '`insistent_https` raised an exception {}'.format(err)
            assert False, err_msg
    # end def

    def test_correct_params_with_args(self, correct_params_with_args: dict):
        try:
            insistent_https(
                server=correct_params_with_args['server'],
                server_path=correct_params_with_args['server_path'],
                args=correct_params_with_args['args'],
            )
        except RequestFailError as err:
            err_msg = '`insistent_https` raised an exception {}'.format(err)
            assert False, err_msg
    # end def


    def test_incorrect_params1(self, incorrect_params1: dict):
        with pytest.raises(RequestFailError):
            insistent_https(
                server=incorrect_params1['server'],
                server_path=incorrect_params1['server_path'],
            )
        # end with
    # end def

    def test_incorrect_params2(self, incorrect_params2: dict):
        with pytest.raises(RequestFailError):
            insistent_https(
                server=incorrect_params2['server'],
                server_path=incorrect_params2['server_path'],
            )
        # end with
    # end def
# end class
