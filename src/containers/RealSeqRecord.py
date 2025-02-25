
from src.containers.SeqRecord import SeqRecord

# TODO: stupid class name
# SeqRecord -> HTSRecord,
# RealSeqRecord -> SeqRecord
class RealSeqRecord(SeqRecord):

    def __init__(self):
        raise NotImplementedError()
    # end def

    def get_seq(self) -> str:
        return self.seq
    # end def
# end class
