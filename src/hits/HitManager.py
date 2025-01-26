
import os

from src.containers.HitToDownload import HitToDownload
from src.config.hits import DB_FILE_NAME, SEP, COMMENT_CHAR


class HitManager:

    def __init__(self, classif_dirpath : str):
        self.db_fpath = os.path.join(
            classif_dirpath,
            DB_FILE_NAME
        )

        self.hit_dict = dict()
        if not os.path.exists(self.db_fpath):
            self._init_db_file()
        elif os.path.getsize(self.db_fpath) == 0:
            self._init_db_file()
        else:
            self.hit_dict = self._read_hit_dict()
        # end if
    # end def

    def _init_db_file(self):
        with open(self.db_fpath, 'wt') as output_handle:
            output_handle.write(self._make_db_comment())
            output_handle.write(self._make_db_header())
        # end with
    # end def

    def _read_hit_dict(self):
        with open(self.db_fpath, 'rt') as input_handle:
            lines = tuple(
                filter(
                    _is_not_comment_line,
                    input_handle.readlines()
                )
            )[1:] # and skip the first (header) line
        # end def

        hit_dict = dict()
        for line in lines:
            hit = HitToDownload.from_tsv_row(line)
            hit_dict[hit.accession] = hit
        # end for
        return hit_dict
    # end def

    def _make_db_comment(self) -> str:
        return f'''{COMMENT_CHAR} Here are accessions and names of GenBank records
{COMMENT_CHAR} that can be used as references for anotation by `barapost-local.py`
{COMMENT_CHAR} You are welcome to edit this file by adding,
{COMMENT_CHAR}   removing or muting lines (with adding '{COMMENT_CHAR}' characters in it's beginning, just like this description).
{COMMENT_CHAR} `barapost-local.py` will skip lines muted with '{COMMENT_CHAR}' character.
{COMMENT_CHAR} You can specify your own FASTA files that you want to use as references for `barapost-local.py`.
{COMMENT_CHAR}   To do it, just write your FASTA file's path to this TSV file in new line.
'''
    # end def

    def _make_db_header(self) -> str:
        return SEP.join(HitToDownload.__slots__) + '\n'
    # end def


    def add_hit(self, hit : HitToDownload):
        self.hit_dict[hit.accession] = hit
    # end def


    def increment_hit(self, accession: str, value : int = 1):
        self.hit_dict[accession].increment(value)
    # end def


    def rewrite_db(self):
        with open(self.db_fpath, 'wt') as output_handle:
            output_handle.write(self._make_db_comment())
            output_handle.write(self._make_db_header())
            for hit in self.hit_dict.values():
                output_handle.write(
                    hit.to_tsv_row()
                )
            # end for
        # end with
    # end def
# end class


# TODO: move to util?
def _is_not_comment_line(string : str) -> bool:
    return not string.startswith(COMMENT_CHAR)
# end def
