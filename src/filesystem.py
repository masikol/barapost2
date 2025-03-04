
import os
import sys
import gzip
import glob
import shutil
import logging

# TODO: don't forget to move higher to some config abstraction level
logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)


FASTA_EXTENSIONS = {
    'fasta',
    'fa',
    'fna',
    'fsa',
    'fasta_nt',
    'fa_nt',
    'fna_nt',
    'fsa_nt',
}

FASTQ_EXTENSIONS = {
    'fastq',
    'fq'
}

# Characters not allowes in filenames
_BAD_CHARS = ("/", "\\", ":", "*", "+", "'",
              "?", "\"", "<", ">", "(", ")",
              "[",  "]", "|", ";", "{", "}",)


def is_fasta(file_path : str) -> bool:
    if is_gzipped(file_path):
        file_path = file_path[:-3]
    # end if
    extension = get_file_extension(file_path)
    return extension.lower() in FASTA_EXTENSIONS
# end def


def is_fastq(file_path : str) -> bool:
    if is_gzipped(file_path):
        file_path = file_path[:-3]
    # end if
    extension = get_file_extension(file_path)
    return extension.lower() in FASTQ_EXTENSIONS
# end def


def is_gzipped(file_path : str) -> bool:
    if not file_path.endswith('.gz'):
        return False
    # end if
    return True
# end def


# TODO: call this on arg parsing stage
def stop_if_bad_gzip_file(file_path : str):
    try:
        with gzip.open(file_path, 'rt') as input_handle:
            input_handle.readline()
        # end with
    except gzip.BadGzipFile as err:
        logging.critical('Error: bad gzip file: `{}`'.format(file_path))
        logging.critical(str(err))
        sys.exit(1)
    # end try
# end def


def get_file_extension(file_path : str) -> str:
    return file_path.split('.')[-1]
# end def

# TODO: test
def remove_file_extension(file_path : str) -> str:
    basename = os.path.basename(file_path)
    if not '.' in basename:
        return file_path
    # end if
    return os.path.join(
        os.path.dirname(file_path),
        basename[: basename.rfind('.')]
    )
# end def


def get_hts_file_type(file_path : str) -> str:
    # hts: High Throughput Sequencing
    if is_gzipped(file_path):
        file_path = file_path[:-3]
    # end if
    return get_file_extension(file_path)
# end def


def is_fast5(file_path : str) -> bool:
    extension = get_file_extension(file_path)
    return extension.lower() == 'fast5'
# end def


def is_pod5(file_path : str) -> bool:
    extension = get_file_extension(file_path)
    return extension.lower() == 'pod5'
# end def


# TODO: S/BLOW5 is to be implemented later
# def is_blow5(file_path : str) -> bool:
#     extension = get_file_extension(file_path)
#     return extension.lower() == 'blow5'
# # end def

# TODO: S/BLOW5 is to be implemented later
# def is_slow5(file_path : str) -> bool:
#     extension = get_file_extension(file_path)
#     return extension.lower() == 'slow5'
# # end def


def remove_bad_chars(string : str) -> str:
    # :param string: string to edit;
    # :type string: str;

    # Replace spaces and non-breaking spaces with underscores.
    string = string.replace(' ', '_')
    string = string.replace('\u00A0', '_')

    # Remove all other "bad chars"
    for char in _BAD_CHARS:
        string = string.replace(char, '')
    # end for

    return string
# end def

# TODO: test
def gzip_file(src_fpath : str, dest_fpath : str):
    with open(src_fpath, 'rb') as input_handle, \
         gzip.open(dest_fpath, 'wb') as output_handle:
         shutil.copyfileobj(input_handle, output_handle)
    # end with
# end def


# TODO: test
def empty_dir(dir_path : str):
    paths_ro_rm = glob.glob(
        os.path.join(dir_path, '*')
    )
    for path in paths_ro_rm:
        if os.path.isfile(path):
            os.unlink(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)
        # end if
    # end for
# end def
