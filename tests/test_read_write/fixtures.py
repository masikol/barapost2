
import os

import pytest


_TEST_DATE_DIR_PATH = os.path.join(
    os.path.dirname(__file__),
    'data',
    'test_input'
)


@pytest.fixture(scope='session')
def some_plain_fasta_fpath() -> str:
    return os.path.join(
        _TEST_DATE_DIR_PATH,
        'some_seqs.fasta'
    )
# end def

@pytest.fixture(scope='session')
def some_gzipped_fasta_fpath() -> str:
    return os.path.join(
        _TEST_DATE_DIR_PATH,
        'some_seqs.fasta.gz'
    )
# end def

@pytest.fixture(scope='session')
def some_plain_fastq_fpath() -> str:
    return os.path.join(
        _TEST_DATE_DIR_PATH,
        'some_seqs.fastq'
    )
# end def

@pytest.fixture(scope='session')
def some_gzipped_fastq_fpath() -> str:
    return os.path.join(
        _TEST_DATE_DIR_PATH,
        'some_seqs.fastq.gz'
    )
# end def

@pytest.fixture(scope='session')
def some_pod5_fpath() -> str:
    return os.path.join(
        _TEST_DATE_DIR_PATH,
        'some_reads.pod5'
    )
# end def

@pytest.fixture(scope='session')
def some_fast5_fpath() -> str:
    return os.path.join(
        _TEST_DATE_DIR_PATH,
        'some_reads.fast5'
    )
# end def

# TODO: S/BLOW5 is to be implemented later
# @pytest.fixture(scope='session')
# def some_blow5_fpath() -> str:
#     return os.path.join(
#         _TEST_DATE_DIR_PATH,
#         'some_reads.blow5'
#     )
# # end def

# TODO: S/BLOW5 is to be implemented later
# @pytest.fixture(scope='session')
# def some_slow5_fpath() -> str:
#     return os.path.join(
#         _TEST_DATE_DIR_PATH,
#         'some_reads.slow5'
#     )
# # end def


@pytest.fixture(scope='session')
def tmp_output_dir_path() -> str:
    dir_path = os.path.join(
        os.path.dirname(_TEST_DATE_DIR_PATH),
        'tmp'
    )
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    # end if
    return dir_path
# end def


@pytest.fixture(scope='session')
def mock_classif_label() -> str:
    return 'test'
# end def
