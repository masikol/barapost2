
import os
import re
import time
import logging
from typing import Sequence

from src.containers.SeqRecord import SeqRecord
from src.network.insistent_https import insistent_https
from src.config.remote_blast import PROGRAM, HITLIST_SIZE, DATABASE, \
                                    SERVER, SERVER_PATH, AUTHOR_EMAIL, TOOL_NAME

# TODO: don't forget to move higher to some config abstraction level
logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)


class RemoteBlast:

    def __init__(self,
                 blast_algorithm : str,
                 organisms : Sequence[str],
                 output_dirpath : str):
        # :param blast_algorithm: BLASTn algorithm to use;
        # :param organisms: list of strings performing `nt` database slices;
        self.blast_algorithm = blast_algorithm
        self.organisms = organisms
        self.output_dirpath = output_dirpath
    # end def

    def submit_remote_blast(self, packet : Sequence[SeqRecord]) -> (str, str):
        request_data = self._make_request_data(packet=packet)
        submission_response = insistent_https(
            server=SERVER,
            server_path=SERVER_PATH,
            method='POST',
            args=request_data['payload'],
            headers=request_data['headers']
        )
        request_id, wait_time = self._parse_rid_rtoe(submission_response)
        return request_id, wait_time
    # end def


    def _make_request_data(self,
                           packet : Sequence[SeqRecord]) -> dict:
        # Function configures the submissoin request to BLAST server.
        # See https://blast.ncbi.nlm.nih.gov/doc/blast-help/urlapi.html#urlapi
        #
        # :param packet: FASTA data of query sequences;
        #
        # Returns a dict of the following structure:
        # {
        #     'payload': the_payload_of_the_request (dict),
        #     'headers': headers of thee request (dict)
        # }

        payload_dict = {
            'CMD'            : 'PUT', # Operation to perform
            'PROGRAM'        : PROGRAM, # BLAST program
            'BLAST_PROGRAMS' : self.blast_algorithm,
            'DATABASE'       : DATABASE, # TODO: nt, core_nt, refseq_reference_genomes, refseq_genomes, wgs
            'HITLIST_SIZE'   : HITLIST_SIZE, # we need only the best hit
        }

        payload_dict['QUERY'] = ''.join(
            map(
                lambda sr : '>{}\n{}\n'.format(sr.header, sr.seq), # TODO: make separate function
                packet
            )
        )

        payload_dict['MEGABLAST'] = ''
        if 'megablast' in self.blast_algorithm.lower():
            payload_dict['MEGABLAST'] = 'on'
        # end if

        if AUTHOR_EMAIL != '':
            payload_dict['email'] = AUTHOR_EMAIL # author's email
            payload_dict['tool'] = TOOL_NAME
        # end if

        # TODO: just nt? and other dbs?
        # `nt` database slices:
        # TODO: exclude organisms
        for i, org in enumerate(self.organisms):
            payload_dict[
                'EQ_MENU{}'.format(i if i > 0 else '')
            ] = org
        # end for
        payload_dict['NUM_ORG'] = str(len(self.organisms))

        return {
            'payload' : payload_dict,
            'headers' : {
                'Content-Type' : 'application/x-www-form-urlencoded',
            },
        }
    # end def


    def _parse_rid_rtoe(self, submission_response : str) -> tuple[str, int]:
        try:
            request_id = re.search(r'RID = (.+)', submission_response).group(1)
            # Get time to wait provided by the NCBI server
            wait_time = int(
                re.search(r'RTOE = ([0-9]+)', submission_response).group(1)
            )
        except AttributeError:
            request_denial_response_fpath = self._make_denial_response_fpath()
            with open(request_denial_response_fpath, 'w') as out_handle:
                out_handle.write(submission_response)
            # end with
            logging.error('Seems, the NCBI has denied your request')
            logging.error('Response is in file `{}`'.format(request_denial_response_fpath))
            raise OSError('Seems, the NCBI has denied your request')
        # end try

        return request_id, wait_time
    # end def


    def _make_denial_response_fpath(self) -> str:
        return os.path.join(
            self.output_dirpath,
            'request_denial_response_{}.html'.format(
                time.strftime('%Y%m%d_%H%M%S', time.localtime())
            )
        )
    # end def


    # TODO: do this in prober_kernel
    # def _save_request_cofiguration(self, request_id, packet_size, packet_mode):
    #     # Save temporary data
    #     # TODO: define 'request_configuration.txt' elsewhere
    #     request_configuration = {
    #         'request_id'  : request_id,
    #         'packet_size' : packet_size,
    #         'packet_mode' : packet_mode,
    #     }
    #     request_config_fpath = os.path.join(
    #         self.output_dirpath,
    #         'request_configuration.txt'
    #     )
    #     with open(request_config_fpath, 'w') as out_handle:
    #         json.dump(request_configuration, out_handle)
    #     # end with
    # # end def
# end class
