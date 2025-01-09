
import os
import re
import sys
import time
import json
import logging
from typing import Sequence

from src.time import humane_time
import src.remote_blast.blast_errors as berr
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


    def submit_remote_blast(self, packet : Sequence[SeqRecord]) -> (str, int):
        request_data = self._make_BLAST_PUT_request_data(packet=packet)
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

    def _make_BLAST_PUT_request_data(self,
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

    def _parse_rid_rtoe(self, submission_response : str) -> (str, int):
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


    def retrieve_results(self, request_id : str, wait_time : int) -> str:
        self._wait_till_job_is_ready(request_id, wait_time)
        blast_result = self._request_results(request_id)
        return blast_result
    # end def

    def _wait_till_job_is_ready(self, request_id : str, wait_time : int):
        # TODO: simplify the method
        self._wait_estimated_time(wait_time)

        job_status_request_data = self._make_job_status_request_data(
            request_id=request_id
        )

        more_wait_time, num_dots_printed = 60, 6
        space_count = num_dots_printed + len("(requesting)")

        job_ready = False
        while not job_ready:
            job_status_response = insistent_https(
                server=SERVER,
                server_path=SERVER_PATH,
                method='GET',
                args=job_status_request_data['payload'],
                headers=job_status_request_data['headers']
            )
            job_status = self._parse_job_status(job_status_response, request_id)

            if job_status == 'WAITING':
                sys.stderr.write(
                    '{} - The request is being processed. Waiting{}'.format(
                        humane_time(),
                        ' ' * space_count
                    )
                )
                sys.stderr.flush()
                # Wait for more_wait_time sec and indicate each 10 seconds with a dot
                for i in range(num_dots_printed):
                    time.sleep(more_wait_time // num_dots_printed)
                    sys.stderr.write('.')
                    sys.stderr.flush()
                # end for
                sys.stderr.write('(requesting)')
                sys.stderr.flush()
                continue

            elif job_status == 'READY':
                job_ready = True
                sys.stderr.write('\n')
                sys.stderr.flush()
                logging.info('Job is ready!')
                if "ThereAreHits=yes" in job_status_response:
                    for i in range(15, 0, -5):
                        sys.stderr.write('-' * i + '\n')
                    # end for
                    logging.info('There are hits!')
                    # TODO: Retrieve human-readable text and put it into result directory ???
                elif "ThereAreHits=no" in job_status_response:
                    # if there are no hits
                    logging.info('There are no hits. It happens.')
                else:
                    # Probably, job has failed if execution reaches here
                    logging.warning(
                        'Job {} has failed. I will split it and resubmit' \
                            .format(request_id)
                    )
                    raise berr.BlastError(berr.ACTION_SPLIT_AND_RESEND)
                # end if

            elif job_status == 'UNKNOWN':
                # Job expired
                logging.info(
                    'Job {} has expired. I will resubmit it' \
                        .format(request_id)
                )
                raise berr.BlastError(berr.ACTION_RESEND)

            elif job_status == 'FAILED':
                # Job failed
                logging.warning(
                    'Job {} has failed. I will split it and resubmit' \
                        .format(request_id)
                )
                raise berr.BlastError(berr.ACTION_SPLIT_AND_RESEND)

            else:
                logging.critical(
                    'Invalid job status for request {}: `{}`' \
                        .format(request_id, job_status)
                )
                raise berr.BlastError(berr.ACTION_PANIC)
            # end if
        # end while
    # end def

    def _wait_estimated_time(self, wait_time : int):
        # TODO: maintain the comment
        # wait_time can be zero at the very beginning of resumption
        if wait_time > 0:
            extra_seconds = 3
            logging.info(
                'BLAST server estimates that alignment'
                ' will be ready in {} seconds'.format(wait_time)
            )
            logging.info(
                'Waiting for {}+{} (+{} extra) seconds...' \
                    .format(wait_time, extra_seconds, extra_seconds)
            )
            # Server migth be wrong -- we will give it 3 extra seconds
            time.sleep(wait_time + extra_seconds)
            logging.info(
                '{} seconds have passed. Checking if the alignment is ready...' \
                    .format(wait_time + extra_seconds)
            )
        # end if
    # end def

    def _make_job_status_request_data(self, request_id : str) -> dict:
        # Example:
        # blast.ncbi.nlm.nih.gov/blast/Blast.cgi?CMD=Get&FORMAT_OBJECT=SearchInfo&RID=S078JZV1013
        payload_dict = {
            'CMD'           : 'GET', # Operation to perform
            'FORMAT_OBJECT' : 'SearchInfo',
            'RID'           : request_id, # Request ID
        }
        return {
            'payload' : payload_dict,
            'headers' : {
                'Content-Type' : 'application/x-www-form-urlencoded',
            },
        }
    # end def

    def _parse_job_status(self,
                          job_status_response : str,
                          request_id : str) -> str:
        job_status_pattern = r'Status=([a-zA-Z]+)'
        re_search_result = re.search(job_status_pattern, job_status_response)
        if re_search_result is None:
            raise ValueError(
                'Cannot parse job status for request {}'.format(request_id)
            )
        # end if
        job_status = re_search_result.group(1).upper()
        return job_status
    # end def

    def _request_results(self, request_id : str) -> dict:
        logging.info('Retrieving results...')
        request_data = self._make_retrieve_request_data(request_id)
        blast_results_raw = insistent_https(
            server=SERVER,
            server_path=SERVER_PATH,
            method='GET',
            args=request_data['payload'],
            headers=request_data['headers']
        )
        return self._parse_blast_results(blast_results_raw)
    # end def

    def _make_retrieve_request_data(self, request_id : str) -> dict:
        # Example:
        # https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=GET&FORMAT_OBJECT=Alignment&RID=S078JZV1013&FORMAT_TYPE=JSON2_S
        payload_dict = {
            'CMD'           : 'GET', # Operation to perform
            'FORMAT_OBJECT' : 'Alignment',
            'RID'           : request_id, # Request ID
            'FORMAT_TYPE'   : 'JSON2_S',
        }
        return {
            'payload' : payload_dict,
            'headers' : {
                'Content-Type' : 'application/x-www-form-urlencoded',
            },
        }
    # end def

    def _parse_blast_results(self, blast_results_raw : str) -> dict:
        try:
            return json.loads(blast_results_raw)
        except (JSONDecodeError, UnicodeDecodeError) as err:
            error_fpath = self._make_problematic_results_fpath()
            logging.critical(
                'Cannot parse results: {}. Writing the results to the file `{}`' \
                    .format(err, error_fpath)
            )
            with open(error_fpath, 'wt') as out_handle:
                out_handle.write(blast_results_raw)
            # end with
            raise berr.BlastError(berr.ACTION_PANIC)
        # end try
    # end def

    def _make_problematic_results_fpath(self) -> str:
        return os.path.join(
            self.output_dirpath,
            'problematic_raw_results.txt'
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
