
from src.containers.SeqRecord import SeqRecord


class ClassifContainer:

    __slots__ = ('record', 'label')

    def __init__(self, record : SeqRecord, label : str):
        self.record = record
        self.label = label
    # end def
# end class
