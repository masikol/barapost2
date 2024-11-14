
import time
import socket
import logging
import http.client

from src.network.RequestFailError import RequestFailError


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
                        url : str,
                        request_for : str = None,
                        accession_number : str = None,
                        timeout : int = 30) -> str:
    # Function performs an 'insistent' HTTPS request.
    # It means that the function tries to get the response
    #     again and again if the request fails.
    #
    # :param server: server address;
    # :param url: the rest of url;
    # :param request_for: a comment for an error message, if applicable;
    # :param accession_number: NCBI accession number being requested, if applicable;
    # :param timeout: timeout;

    # We can get spurious 404 or sth due to instability of NCBI servers work.
    # Let's give it 3 attempts (with some sleep time in between),
    #   and if all them are unsuccessful -- raise an error.
    error = True
    sleep_time = 30
    attempt_i, max_attempts = 0, 3

    while error:

        response = None

        try:
            conn = http.client.HTTPSConnection(server, timeout=timeout)
            conn.request('GET', url)
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
            if attempt_i < max_attempts:
                logging_str += '{} attempts to connect left, waiting for {} sec... ' \
                    .format(max_attempts - attempt_i, sleep_time)
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
