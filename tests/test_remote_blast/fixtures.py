
import os
from typing import Sequence

import pytest

from src.containers import Fasta
from src.reader_system.ReaderWrapper import ReaderWrapper


# >>> Auxiliary functions >>>

def read_first_fasta_seq(input_fpath : str) -> Fasta:
    reader_wrapper = ReaderWrapper(
        file_paths=[input_fpath],
        packet_size=1,
        probing_batch_size=1,
        mode='seq_count'
    )
    with reader_wrapper as input_handle:
        for container_packet in input_handle:
            result_container = next(iter(container_packet))
            break
        # end of
    # end with
    return result_container
# end def

# <<< Auxiliary functions <<<


@pytest.fixture(scope='session')
def tmp_outdir() -> str:
    tmp_outdir_path = os.path.join(
        os.path.dirname(__file__),
        'data',
        'test_outdir'
    )
    if not os.path.isdir(tmp_outdir_path):
        os.makedirs(tmp_outdir_path)
    # end if
    return tmp_outdir_path
# end def


@pytest.fixture(scope='session')
def query_seq_1() -> Fasta:
    input_file_path = os.path.join(
        os.path.dirname(__file__),
        'data',
        'query_corona_seq.fasta'
    )
    return read_first_fasta_seq(input_file_path)
# end def


@pytest.fixture(scope='session')
def query_seq_2() -> Fasta:
    input_file_path = os.path.join(
        os.path.dirname(__file__),
        'data',
        '52a41318-f8b9-4d61-a21f-4a907f107973.fasta'
    )
    return read_first_fasta_seq(input_file_path)
# end def


@pytest.fixture(scope='session')
def query_seq_3() -> Fasta:
    input_file_path = os.path.join(
        os.path.dirname(__file__),
        'data',
        '711bf04d-20f5-4418-9712-16168ef98999.fasta'
    )
    return read_first_fasta_seq(input_file_path)
# end def


@pytest.fixture(scope='session')
def test_organisms() -> Sequence[str]:
    return ['561879', '2697049']
# end def


@pytest.fixture(scope='session')
def invalid_request_id():
    return 'T0000000000'
# end def
