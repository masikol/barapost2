
import time


def humane_time() -> str:
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
# end def
