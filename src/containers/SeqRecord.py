
from src.containers.HTSRecord import HTSRecord


class SeqRecord(HTSRecord):

    def __init__(self):
        raise NotImplementedError()
    # end def

    def get_seq(self) -> str:
        return self.seq
    # end def
# end class
