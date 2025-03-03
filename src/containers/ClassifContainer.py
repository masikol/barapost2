
from src.containers.HTSRecord import HTSRecord


class ClassifContainer:

    __slots__ = ('record', 'label')

    def __init__(self, record : HTSRecord, label : str):
        self.record = record
        self.label = label
    # end def
# end class
