
def str_None_rep(sth, None_rep : str = '') -> str:
    # It's a wrapper for str function,
    #     but is handles None is a special way
    return None_rep if sth is None else str(sth)
# end def
