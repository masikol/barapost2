
import os
from typing import Sequence

import pytest

from src.containers import Fasta
from src.remote_blast.remote_blast import RemoteBlast
from src.config.remote_blast import AUTHOR_EMAIL, TOOL_NAME

from tests.test_remote_blast.fixtures import query_seq_1, \
                                             query_seq_2, \
                                             query_seq_3, \
                                             test_organisms, \
                                             tmp_outdir


class TestMakeRequestData:

    def test_request_payload_data_minimal(self,
                                          query_seq_1 : Fasta,
                                          query_seq_2 : Fasta,
                                          query_seq_3 : Fasta,
                                          tmp_outdir : str):
        remote_blast = RemoteBlast(
            blast_algorithm='megaBlast',
            organisms=[],
            output_dirpath=tmp_outdir
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
                                            test_organisms : Sequence[str],
                                            tmp_outdir : str):
        remote_blast = RemoteBlast(
            blast_algorithm='megaBlast',
            organisms=test_organisms,
            output_dirpath=tmp_outdir
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
