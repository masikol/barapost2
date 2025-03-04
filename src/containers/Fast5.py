
from ont_fast5_api.fast5_read import Fast5Read

from src.containers.HTSRecord import HTSRecord


class Fast5(HTSRecord):

    __slots__ = ('record')

    def __init__(self, record : Fast5Read):
        self.record = record
    # end def

    def __str__(self):
        return f'''record : {self.record}.\n'''
    # end def

    def __repr__(self):
        return f'''Fast5(
    record={self.record!r},
)'''
    # end def

    def get_seq_id(self) -> str:
        return self.record.get_read_id()
    # end def
# end class
