
import logging

import src.remote_blast.blast_errors as berr
from src.remote_blast.RemoteBlast import RemoteBlast


# TODO: don't forget to move higher to some config abstraction level
logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)


def ask_for_resumption():
    # Function asks a user if he/she wants to resume the previous run.
    # Returns True if the decision is to resume, else False

    resume = None

    while resume is None:
        resume = input('''
Would you like to resume the previous run?
   1 -- Resume!
   2 -- Start from the beginning.

Enter a number (1 or 2):>> ''')
        # Check if entered value is integer number. If no, give another attempt.
        try:
            resume = int(resume)
            # Check if input number is 1 or 2
            if resume != 1 and resume != 2:
                print('\n   Invalid number entered!\a\n' + '~'*20)
                resume = None
            else:
                if resume == 1:
                    'resume the previous run'
                else:
                    'start from the beginning'
                # end if
                logging.info('You have chosen to {}.'.format(action))
                print()
            # end if
        except ValueError:
            print('\nInvalid value entered!\a\n' + '~'*20)
            resume = None
        # end try

    return resume == 1
# end def
