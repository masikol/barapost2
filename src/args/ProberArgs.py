
import argparse
from typing import Sequence


class ProberArgs:

    # TODO: implement
    # @classmethod
    # def parse(cls) -> 'ProberArgs':
    #     return ProberArgs(

    #     )
    # # end def

    def __init__(self,
                 input_fpaths : Sequence[str],
                 output_dirpath : str,
                 probing_batch_size : int,
                 packet_mode : str = 'seq_count',
                 packet_size : int = 100,
                 max_seq_len : int = None,
                 blast_algorithm : str = 'megaBlast',
                 organisms : Sequence[int] = list()):
        self.input_fpaths       = input_fpaths
        self.output_dirpath     = output_dirpath
        self.probing_batch_size = probing_batch_size
        self.packet_mode        = packet_mode
        self.packet_size        = packet_size
        self.max_seq_len        = max_seq_len
        self.blast_algorithm    = blast_algorithm
        self.organisms          = organisms
    # end def

# end class