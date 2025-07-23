
import os


PACKET_MODE_0 = 'seq_count'
PACKET_MODE_1 = 'sum_seq_len'

BLAST_ALGORITHMS = {
    '0' : 'megaBlast',
    '1' : 'discoMegablast',
    '2' : 'blastn',
}

DEFAULT_PROBING_BATCH_SIZE = 200
DEFAULT_PACKET_MODE = PACKET_MODE_0
DEFAULT_PACKET_SIZE = 100
DEFAULT_BLAST_ALGORITHM = '0'
DEFAULT_PHRED_OFFSET = 33
DEFAULT_OUTDIR_PATH = os.path.join(os.getcwd(), 'barapost_result')
