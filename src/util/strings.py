
from typing import Any

def str_None_rep(sth : Any, None_rep : str = '') -> str:
    # It's a wrapper for str function,
    #     but is handles None is a special way
    return None_rep if sth is None else str(sth)
# end def


def is_comment_line(string : str, comment_char : str = '#') -> bool:
    return string.lstrip().startswith(comment_char)
# end def
