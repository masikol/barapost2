
import time
import socket
import logging
import http.client
import urllib.parse

from src.network.RequestFailError import RequestFailError
from src.config.network_config import MAX_ATTEMPT_COUNT, DEFAULT_TIMEOUT


# TODO: don't forget to move higher to some config abstraction level
logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)


# TODO: ???
# try:
#     import ssl
# except ImportError:
#     pass
# else:
#     ssl._create_default_https_context = ssl._create_unverified_context
# # end try


def insistent_https_get(server : str,
                        server_path : str,
                        args : dict = dict(),
                        request_for : str = None,
                        accession_number : str = None) -> str:
    # Function performs an 'insistent' HTTPS request.
    # It means that the function performs queries
    #     several times if the request fails.
    #
    # ncbi.nlm.nih.gov/nuccore/CP045701.2?report=gilist&format=text
    # ~~~~~~~~~~~~~~~~                    ~~~~~~~~~~~~~~~~~~~~~~~~~
    #                 ~~~~~~~~~~~~~~~~~~~
    # ^ server        ^ server_path       ^ args (urlencoded)
    # 
    # :param server: server address;
    # :param server_path: path within the server;
    # :param args: get argument dictionary;
    # :param request_for: a comment for an error message, if applicable.
    #        It's for making potential error messages more informative;
    # :param accession_number: NCBI accession number being requested, if applicable.
    #        It's for making potential error messages more informative;

    error = True
    sleep_time = 30 # s
    attempt_i = 0

    path_and_args = server_path
    if len(args) > 0:
        path_and_args = '{}?{}'.format(
            path_and_args,
            urllib.parse.urlencode(args)
        )
    # end if

    while error:

        response = None

        try:
            conn = http.client.HTTPSConnection(server, timeout=DEFAULT_TIMEOUT)
            conn.request('GET', path_and_args)
            response = conn.getresponse()
            if response.code != 200:
                raise RequestFailError
            # end if

        except (OSError, \
                socket.gaierror, \
                RequestFailError, \
                http.client.CannotSendRequest, \
                http.client.RemoteDisconnected) as err:
            logging_str = 'Error. Cannot retrieve data: {}. '.format(str(err))
            if not response is None:
                logging_str += 'Response code: {}. Error reason provided: "{}". ' \
                    .format(response.code, response.reason)
            # end if
            if not request_for is None:
                logging_str += 'Request for {} has failed. '.format(request_for)
            # end if
            if not accession_number is None:
                logging_str += 'Accession being requested: `{}`. '.format(
                    accession_number
                )
            # end if
            if 'ncbi.nlm.nih.gov' in server:
                logging_str += 'It may be due to instable work of NCBI servers. '
            # end if
            if attempt_i < MAX_ATTEMPT_COUNT:
                logging_str += '{} attempts to connect left, waiting for {} sec... ' \
                    .format(MAX_ATTEMPT_COUNT - attempt_i, sleep_time)
                logging.warning(logging_str)
                attempt_i += 1
                time.sleep(sleep_time)
            else:
                logging.error(logging_str)
                raise RequestFailError
            # end if

        else:
            error = False # leave the loop
            resp_content = str(response.read(), 'utf-8')

        finally:
            conn.close()
        # end try
    # end while

    return resp_content
# end def
