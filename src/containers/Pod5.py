
from src.containers.HTSRecord import HTSRecord
from pod5 import ReadRecord


class Pod5(HTSRecord):

    __slots__ = ('record')

    def __init__(self, record : ReadRecord):
        self.record = record
    # end def

    def __str__(self):
        return f'record : {self.record}'
    # end def

    def __repr__(self):
        return f'''Pod5(
    record={self.record!r}
)'''
    # end def

    def get_seq_id(self) -> str:
        return str(self.record.read_id)
    # end def
# end class
