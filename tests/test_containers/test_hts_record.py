
import os

import pytest
from pod5 import DatasetReader
from ont_fast5_api.fast5_interface import get_fast5_file

from src.containers.Fasta import Fasta
from src.containers.Fastq import Fastq
from src.containers.Pod5  import Pod5
from src.containers.Fast5 import Fast5


RANDOM_HEADER = 'pretty_woman'


@pytest.fixture
def some_fasta_record() -> Fasta:
    return Fasta(
        header=RANDOM_HEADER,
        seq='CATGATGCTAGC'
    )
# end def

@pytest.fixture
def some_fastq_record() -> Fasta:
    seq = 'CATGATGCTAGC'
    return Fastq(
        header=RANDOM_HEADER,
        seq=seq,
        comment='+',
        quality='7' * len(seq)
    )
# end def


@pytest.fixture
def some_pod5_record() -> Pod5:
    pod5_fpath = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'test_read_write',
        'data',
        'test_input',
        'some_reads.pod5'
    )
    with DatasetReader(pod5_fpath) as input_handle:
        record = next(iter(input_handle.reads()))
    # end def
    return Pod5(record=record)
# end def


@pytest.fixture
def some_fast5_record() -> Fast5:
    fast5_fpath = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'test_read_write',
        'data',
        'test_input',
        'some_reads.fast5'
    )
    with get_fast5_file(fast5_fpath) as input_handle:
        record = next(iter(input_handle.get_reads()))
    # end def
    return Fast5(record=record)
# end def


class TestHTSRecord:

    def test_get_seq_id_fasta(self, some_fasta_record : Fasta):
        assert some_fasta_record.get_seq_id() == RANDOM_HEADER
    # end def

    def test_get_seq_id_fastq(self, some_fastq_record : Fastq):
        assert some_fastq_record.get_seq_id() == RANDOM_HEADER
    # end def

    def test_get_seq_id_pod5(self, some_pod5_record : Pod5):
        # Got directly from the file
        expected = 'c018e0f4-2cf9-4b36-8961-751cc03d8dd5'
        obtained = some_pod5_record.get_seq_id()
        assert obtained == expected
    # end def

    def test_get_seq_id_fast5(self, some_fast5_record : Fast5):
        # Got directly from the file
        expected = '00001da1-4ebb-4ce6-9128-d050d3696fcc'
        obtained = some_fast5_record.get_seq_id()
        assert obtained == expected
    # end def

# end def
