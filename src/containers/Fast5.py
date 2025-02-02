
# TODO: remove
# from h5py import File
from ont_fast5_api.fast5_read import Fast5Read

from src.containers.SeqRecord import SeqRecord


class Fast5(SeqRecord):

    __slots__ = ('read_data')

    def __init__(self, read_data : Fast5Read):
        self.read_data = read_data
    # end def

    def __str__(self):
        return f'''read_data : {self.read_data}.\n'''
    # end def

    def __repr__(self):
        return f'''Fast5(
    read_data={self.read_data!r},
)'''
    # end def
# end class
