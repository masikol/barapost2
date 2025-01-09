
from typing import TypeAlias


action_code : TypeAlias = int

ACTION_OK_RETIEVE       : action_code = 0
ACTION_RESEND           : action_code = 1
ACTION_SPLIT_AND_RESEND : action_code = 2
ACTION_PANIC            : action_code = 3


class BlastError:
    def __init__(self, code: action_code):
        self.code = code
    # end def
# end class
