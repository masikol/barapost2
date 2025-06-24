
import re
import os

import src.filesystem as fs
from src.util.strings import is_comment_line
from src.containers.SeqTaxonomy import SeqTaxonomy
from src.taxonomy.TaxonomySearcher import TaxonomySearcher
from src.config.taxonomy import TAXONOMY_SEP, \
                                COMMENT_CHAR, \
                                DB_FILE_NAME, \
                                OWN_SEQ_TAX_SEP, \
                                TAXONOMY_COLNAMES, \
                                OWN_SEQ_TAXONOMY_FMT, \
                                RANKS_SORTED_DESCENDING


def _is_not_taxonomy_comment_line(string : str) -> bool:
    return is_comment_line(string, COMMENT_CHAR)
# end def


class TaxonomyManager:

    def __init__(self, work_dirpath : str):
        self._db_fpath = os.path.join(
            work_dirpath,
            DB_FILE_NAME
        )
        self._taxonomy_searcher = TaxonomySearcher()

        if not os.path.isfile(self._db_fpath) \
           or os.path.getsize(self._db_fpath) == 0:
            self._init_tax_file()
            self.taxonomy_dict = dict()
        # end if
        self.taxonomy_dict = self._read_taxonomy_dict()
    # end def

    def _init_tax_file(self):
        with open(self._db_fpath, 'wt') as out_handle:
            out_handle.write(
                '{}\n'.format(
                    TAXONOMY_SEP.join(TAXONOMY_COLNAMES)
                )
            )
        # end with
    # end def

    def _read_taxonomy_dict(self) -> dict:

        with open(self._db_fpath, 'rt') as input_handle:
            lines = tuple(
                filter(
                    _is_not_taxonomy_comment_line,
                    input_handle.readlines()
                )
            )[1:] # and skip the first (header) line
        # end def

        taxonomy_dict = dict()
        for line in lines:
            seq_taxonomy = SeqTaxonomy.from_tsv_row(line.strip())
            taxonomy_dict[seq_taxonomy.seq_id] = seq_taxonomy
        # end for
        return taxonomy_dict
    # end def


    def add_taxonomy(self, seq_id : str, seq_taxonomy : SeqTaxonomy = None):
        seq_id_is_new = not seq_id in self.taxonomy_dict
        if seq_id_is_new:
            if seq_taxonomy is None:
                seq_taxonomy = self._taxonomy_searcher.search_taxonomy(seq_id)
            # end if
            self.taxonomy_dict[seq_id] = seq_taxonomy
        # end if
    # end def

    def rewrite_taxonomy_file(self):
        self._init_tax_file()
        with open(self._db_fpath, 'at') as out_handle:
            for seq_taxonomy in self.taxonomy_dict.values():
                out_handle.write(
                    seq_taxonomy.to_tsv_row()
                )
            # end for
        # end with
    # end def

    # TODO: move to some other class?
    def parse_own_seq_taxonomy(self,
                               seq_id : str,
                               haystack_str : str) -> SeqTaxonomy:
        # Function parses ID of user's reference sequence and forms a taxonomy tuple
        #   if there is proper taxonomy string in ID line in fasta format.
        # "Proper" taxonomy string is following:
        #   '[ANYTHING BEFORE] <Domain>;<Phylum>;<Class>;<Order>;<Family>;<Genus>;<species> [ANYTHING AFTER]'
        # Spaces are not allowed. Ranks can be omitted in manner like this
        #   (order and species is missing):
        #   '[ANYTHING BEFORE] <Domain>;<Phylum>;<Class>;;<Family>;<Genus>; [ANYTHING AFTER]'
        # If there is no taxonomy string in sequence ID, we'll merely save this ID to taxonomy file.
        #
        # :param seq_id: sequence ID (e.g. accession number);
        # :type seq_id: str;
        # :param haystack_str: a string to parse;
        # :type haystack_str: str;
        #
        # Returns taxonomy string.

        # Check if `haystack_str` matches `OWN_SEQ_TAXONOMY_FMT`
        own_seq_tax_match = re.search(OWN_SEQ_TAXONOMY_FMT, haystack_str)

        # If there is a match and it taxonomic names are not empty,
        #   form taxonomic tuple:
        empty_tax_str = OWN_SEQ_TAX_SEP * (len(RANKS_SORTED_DESCENDING)-1)
        own_seq_taxonomy_found = not own_seq_tax_match is None \
                                 and own_seq_tax_match.group(0) != empty_tax_str
        if own_seq_taxonomy_found:
            taxonomy_str = own_seq_tax_match.group(0)
            seq_taxonomy = SeqTaxonomy.from_own_seq_tax_str(
                seq_id=seq_id,
                own_seq_tax_str=taxonomy_str,
                sep=OWN_SEQ_TAX_SEP
            )
        else:
            # Otherwise we will merely use this haystack_str as a label
            taxonomy_str = fs.remove_bad_chars(haystack_str)
            seq_taxonomy = SeqTaxonomy.from_arbitrary_label(
                seq_id=seq_id,
                label=taxonomy_str
            )
        # end if

        return seq_taxonomy
    # end def


    # TODO: LATER: add this function, but, uh, later; not sure about this
    # def recover_taxonomy(acc, hit_def, taxonomy_path):
    #     # Function recovers missing taxonomy by given accession.
    #     #
    #     # :param acc: accession of taxonomy entry to recover;
    #     # :type acc: str;
    #     # :param hit_def: name of this sequence;
    #     # :type hit_def: sre;
    #     # :param taxonomy_path: path to TSV file with taxonomy;
    #     # :type taxonomy_path: str;

    #     if acc == "LAMBDA":
    #         # If we are missing lambda phage taxonomy -- just add it
    #         save_taxonomy_directly(taxonomy_path, acc, "Lambda-phage-nanopore-control")
    #     elif acc.startswith("OWN_SEQ_"):
    #         # If sequence is an "own seq" -- check fasta file

    #         # Get necessary title line from `local_seq_set.fasta`
    #         # Firstly find fasta file (it may be compressed)
    #         classif_dir = os.path.dirname(os.path.dirname(taxonomy_path))
    #         db_dir = os.path.join(classif_dir, "local_database")
    #         db_files = glob.glob("{}{}*".format(db_dir, os.sep))
    #         try:
    #             local_fasta = next(iter(filter(is_fasta, db_files)))
    #         except StopIteration:
    #             printlog_error_time("Error: cannot recover taxonomy for following sequence:")
    #             printlog_error(" `{} - {}`.".format(acc, hit_def))
    #             printlog_error("You can solve this problem by yourself (it's pretty simple).")
    #             printlog_error("Just add taxonomy line for {} to file `{}`".format(acc, taxonomy_path))
    #             printlog_error("  and run the program again.")
    #             platf_depend_exit(1)
    #         # end try

    #         # Find our line startingg with `acc`
    #         how_to_open = OPEN_FUNCS[is_gzipped(local_fasta)]
    #         fmt_func = FORMATTING_FUNCS[is_gzipped(local_fasta)]
    #         if is_gzipped(local_fasta):
    #             search_for = b">" + bytes(acc, 'ascii') + b" "
    #         else:
    #             search_for = ">{} ".format(acc)
    #         # end if

    #         with how_to_open(local_fasta) as fasta_file:
    #             for line in fasta_file:
    #                 if line.startswith(search_for):
    #                     seq_name = fmt_func(line).partition(' ')[2] # get name of the sequence
    #                     save_taxonomy_directly(taxonomy_path, acc, seq_name)
    #                     break
    #                 # end if
    #             # end for
    #         # end with
    #     else:
    #         # Try to find taxonomy in NCBI
    #         download_taxonomy(acc, hit_def, taxonomy_path)
    #     # end if
    # # end def
# end class
