
import os
from typing import Sequence

import pytest

from src.containers import Fasta
from src.remote_blast.remote_blast import RemoteBlast
from src.reader_system.ReaderWrapper import ReaderWrapper
from src.config.remote_blast import AUTHOR_EMAIL, TOOL_NAME


# === Configuration ===

TMP_OUTDIR = os.path.join(
    os.path.dirname(__file__),
    'data',
    'test_outdir'
)
if not os.path.isdir(TMP_OUTDIR):
    os.makedirs(TMP_OUTDIR)
# end if


# === Auxiliary functions ===

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


# === Fixtures ===

@pytest.fixture
def query_seq_1() -> Fasta:
    input_file_path = os.path.join(
        os.path.dirname(__file__),
        'data',
        'query_corona_seq.fasta'
    )
    return read_first_fasta_seq(input_file_path)
# end def

@pytest.fixture
def query_seq_2() -> Fasta:
    input_file_path = os.path.join(
        os.path.dirname(__file__),
        'data',
        '52a41318-f8b9-4d61-a21f-4a907f107973.fasta'
    )
    return read_first_fasta_seq(input_file_path)
# end def

@pytest.fixture
def query_seq_3() -> Fasta:
    input_file_path = os.path.join(
        os.path.dirname(__file__),
        'data',
        '711bf04d-20f5-4418-9712-16168ef98999.fasta'
    )
    return read_first_fasta_seq(input_file_path)
# end def

@pytest.fixture
def test_organisms() -> Sequence[str]:
    return ['561879', '2697049']
# end def


# === Test classes ===

class TestMakeRequestData:

    def test_request_payload_data_minimal(self,
                                          query_seq_1 : Fasta,
                                          query_seq_2 : Fasta,
                                          query_seq_3 : Fasta):
        remote_blast = RemoteBlast(
            blast_algorithm='megaBlast',
            organisms=[],
            output_dirpath=TMP_OUTDIR
        )
        request_data : dict = remote_blast._make_BLAST_PUT_request_data(
            packet=[query_seq_1, query_seq_2, query_seq_3,]
        )

        assert 'payload' in request_data
        assert 'headers' in request_data
        assert type(request_data['payload']) == dict
        assert type(request_data['headers']) == dict

        payload_required_keys = (
            'CMD',
            'PROGRAM',
            'BLAST_PROGRAMS',
            'DATABASE',
            'HITLIST_SIZE',
            'QUERY',
            'MEGABLAST',
        )
        for k in payload_required_keys:
            assert k in request_data['payload']
        # end for

        assert 'email' in request_data['payload']
        assert 'tool' in request_data['payload']
        assert request_data['payload']['email'] == AUTHOR_EMAIL
        assert request_data['payload']['tool'] == TOOL_NAME

        assert 'Content-Type' in request_data['headers']
    # end def


    def test_request_payload_data_organisms(self,
                                            query_seq_1 : Fasta,
                                            query_seq_2 : Fasta,
                                            query_seq_3 : Fasta,
                                            test_organisms : Sequence[str]):
        remote_blast = RemoteBlast(
            blast_algorithm='megaBlast',
            organisms=test_organisms,
            output_dirpath=TMP_OUTDIR
        )
        request_data : dict = remote_blast._make_BLAST_PUT_request_data(
            packet=[query_seq_1, query_seq_2, query_seq_3,]
        )

        assert 'NUM_ORG' in request_data['payload']
        assert int(request_data['payload']['NUM_ORG']) == 2
        assert request_data['payload']['EQ_MENU'] == test_organisms[0]
        assert request_data['payload']['EQ_MENU1'] == test_organisms[1]
    # end def
# end class
