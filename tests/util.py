
import os
import glob
import gzip
import hashlib

import pod5 as p5
from ont_fast5_api.fast5_interface import get_fast5_file


def md5_file_sum(file_path : str) -> str:
    with open(file_path, 'rb') as input_handle:
        digest = hashlib.file_digest(input_handle, 'md5')
    # end with
    return digest.hexdigest()
# end def

def md5_gzipped_file_sum(file_path : str) -> str:
    with gzip.open(file_path, 'rb') as input_handle:
        digest = hashlib.file_digest(input_handle, 'md5')
    # end with
    return digest.hexdigest()
# end def

def md5_sum(string : str) -> str:
    return hashlib.md5(
        string.encode('utf-8')
    ).hexdigest()
# end def

def md5_pod5_file(file_path : str) -> str:
    with p5.Reader(file_path) as reader:
        string_for_hash = '$'.join(
            map(
                lambda read: '$'.join(
                    [str(read.read_id), str(read.sample_count),]
                ),
                reader.reads()
            )
        )
    # end for
    return md5_sum(string_for_hash)
# end def

def md5_fast5_file(file_path : str) -> str:
    with get_fast5_file(file_path, mode='r') as reader:
        string_for_hash = '$'.join(
            map(
                lambda read: '$'.join(
                    [str(read.read_id), str(read.get_raw_data()),]
                ),
                reader.get_reads()
            )
        )
    # end for
    return md5_sum(string_for_hash)
# end def



def clear_dir(dir_path : str):
    for fpath in glob.iglob(os.path.join(dir_path, '*')):
        os.unlink(fpath)
    # end for
# end def
