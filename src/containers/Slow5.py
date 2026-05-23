
from src.containers.HTSRecord import HTSRecord

# TODO: LATER: S/BLOW5 is to be implemented later
class Slow5(HTSRecord):

    __slots__ = ('record')

    def __init__(self, record : dict) -> None:
        self.record = record.copy()
    # end def

    def __str__(self) -> str:
        return f'record : {self.record}'
    # end def

    def __repr__(self) -> str:
        return f'''Slow5(
    record={self.record!r}
)'''
    # end def
# end class
