
from typing import Sequence

import pytest

from src.containers import Fasta
import src.remote_blast.blast_errors as berr
from src.containers.AlignResult import AlignResult
from src.remote_blast.RemoteBlast import RemoteBlast

from tests.test_remote_blast.fixtures import query_seq_1, \
                                             query_seq_2, \
                                             query_seq_3, \
                                             test_organisms, \
                                             tmp_outdir, \
                                             invalid_request_id

class TestRemoteBlast:

    def test_basic_remote_blast(self,
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
        packet = [query_seq_1, query_seq_2, query_seq_3,]
        request_id, wait_time = remote_blast.submit_remote_blast(packet)

        try:
            result = remote_blast.retrieve_results(request_id, wait_time)
        except berr.BlastError as err:
            assert False, f'Error in test_basic_remote_blast: {err}'
        # end try

        assert len(result) == 3
        assert type(
            next(iter(result)) == AlignResult
        )

        first_align_result = next(
            iter(
                result[query_seq_1.header]
            )
        )
        assert not first_align_result.hit_accession is None

        first_align_result = next(
            iter(
                result[query_seq_2.header]
            )
        )
        assert not first_align_result.hit_accession is None

        first_align_result = next(
            iter(
                result[query_seq_3.header]
            )
        )
        assert first_align_result.hit_accession is None
    # end def


    def test_remote_blast_no_hits(self,
                                  query_seq_3 : Fasta,
                                  test_organisms : Sequence[str],
                                  tmp_outdir : str):
        # query_seq_3 should end in no hits
        #   and BlastError(ACTION_NO_HITS)
        remote_blast = RemoteBlast(
            blast_algorithm='megaBlast',
            organisms=test_organisms,
            output_dirpath=tmp_outdir
        )
        packet = [query_seq_3,]
        request_id, wait_time = remote_blast.submit_remote_blast(packet)
        with pytest.raises(berr.BlastError) as excinfo:
            remote_blast.retrieve_results(request_id, wait_time)
        # end with
        assert excinfo.value.code == berr.ACTION_NO_HITS
    # end def


    def test_remote_blast_expired(self,
                                  test_organisms : Sequence[str],
                                  tmp_outdir : str,
                                  invalid_request_id : str):
        # Invalid and expired request_ids should end in
        #   "expired job", and BlastError(ACTION_RESEND)

        remote_blast = RemoteBlast(
            blast_algorithm='megaBlast',
            organisms=test_organisms,
            output_dirpath=tmp_outdir
        )

        requiest_id = invalid_request_id
        wait_time = 1
        with pytest.raises(berr.BlastError) as excinfo:
            remote_blast.retrieve_results(requiest_id, wait_time)
        # end with
        assert excinfo.value.code == berr.ACTION_RESEND
    # end def
# end class
