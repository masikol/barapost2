
from typing import Sequence
from functools import reduce

from src.taxonomy.taxonomy_config import TAXONOMY_SEP, \
                                         OWN_SEQ_TAX_SEP, \
                                         TAXONOMY_COLNAMES, \
                                         RANKS_SORTED_DESCENDING


class SeqTaxonomy:

    __slots__ = TAXONOMY_COLNAMES

    def __init__(self,
                 seq_id   : str,
                 rank     : str,
                 tax_name : str = None,
                 Domain   : str = None,
                 Phylum   : str = None,
                 Class    : str = None,
                 Order    : str = None,
                 Family   : str = None,
                 Genus    : str = None,
                 Species  : str = None):
        self.seq_id   = seq_id
        self.rank     = rank
        self.tax_name = tax_name
        self.Domain   = Domain
        self.Phylum   = Phylum
        self.Class    = Class
        self.Order    = Order
        self.Family   = Family
        self.Genus    = Genus
        self.Species  = Species
    # end def

    @classmethod
    def from_tsv_row(cls,
                     row_str : str,
                     sep : str = TAXONOMY_SEP) -> 'SeqTaxonomy':
        split_row = row_str.split(sep)
        split_row = tuple(
            map(
                lambda x: None if x == '' else x.strip(),
                split_row
            )
        )
        return SeqTaxonomy(
            seq_id=split_row[0],
            rank=split_row[1],
            tax_name=split_row[2],
            Domain=split_row[3],
            Phylum=split_row[4],
            Class=split_row[5],
            Order=split_row[6],
            Family=split_row[7],
            Genus=split_row[8],
            Species=split_row[9],
        )
    # end def

    @classmethod
    def from_own_seq_tax_str(cls,
                             seq_id : str,
                             own_seq_tax_str : str,
                             sep : str = OWN_SEQ_TAX_SEP) -> 'SeqTaxonomy':
        split_row = own_seq_tax_str.split(sep)
        split_row = tuple(
            map(
                lambda x: None if x == '' else x.strip(),
                split_row
            )
        )

        rank, tax_name = cls._infer_own_seq_rank_and_tax_name(split_row)
        if tax_name is None:
            tax_name = seq_id
        # end if

        return SeqTaxonomy(
            seq_id=seq_id,
            rank=rank,
            tax_name=tax_name,
            Domain=split_row[0],
            Phylum=split_row[1],
            Class=split_row[2],
            Order=split_row[3],
            Family=split_row[4],
            Genus=split_row[5],
            Species=split_row[6],
        )
    # end def

    @classmethod
    def _infer_own_seq_rank_and_tax_name(cls, split_row : Sequence[str]) -> str:
        own_seq_names = (
            split_row[6], split_row[5], split_row[4],
            split_row[3], split_row[2], split_row[1],
            split_row[0],
        )
        ranks = reversed(RANKS_SORTED_DESCENDING)
        for rank, tax_name in zip(ranks, own_seq_names):
            if not tax_name is None:
                return rank, tax_name
            # end if
        # end def
        return None, None
    # end def

    @classmethod
    def from_arbitrary_label(cls, seq_id : str, label : str) -> 'SeqTaxonomy':
        return SeqTaxonomy(
            seq_id=seq_id,
            rank=None,
            tax_name=label,
            Domain=None,
            Phylum=None,
            Class=None,
            Order=None,
            Family=None,
            Genus=None,
            Species=None,
        )
    # end def

    def to_tsv_row(self, sep : str = TAXONOMY_SEP) -> str:
        values = map(
            _str_None_rep,
            (
                self.seq_id,
                self.rank,
                self.tax_name,
                self.Domain,
                self.Phylum,
                self.Class,
                self.Order,
                self.Family,
                self.Genus,
                self.Species,
            )
        )
        return '{}\n'.format(sep.join(values))
    # end def


    def is_empty(self) -> bool:
        return all(
            map(
                lambda x: x is None,
                (
                    self.Domain,
                    self.Phylum,
                    self.Class,
                    self.Order,
                    self.Family,
                    self.Genus,
                    self.Species,
                )
            )
        )
    # end def


    def __eq__(self, other) -> bool:
        return self.seq_id       == other.seq_id \
               and self.rank     == other.rank \
               and self.tax_name == other.tax_name \
               and self.Domain   == other.Domain \
               and self.Phylum   == other.Phylum \
               and self.Class    == other.Class \
               and self.Order    == other.Order \
               and self.Family   == other.Family \
               and self.Genus    == other.Genus \
               and self.Species  == other.Species
    # end def

    def __str__(self) -> str:
        return 'seq_id : `{}`, ' \
               'rank : `{}`, ' \
               'tax_name : `{}`, ' \
               'Domain : `{}`, ' \
               'Phylum : `{}`, ' \
               'Class : `{}`, ' \
               'Order : `{}`, ' \
               'Family : `{}`, ' \
               'Genus : `{}`, ' \
               'Species : `{}`' \
               .format(
                   self.seq_id,
                   self.rank,
                   self.tax_name,
                   self.Domain,
                   self.Phylum,
                   self.Class,
                   self.Order,
                   self.Family,
                   self.Genus,
                   self.Species
               )
    # end def

    # TODO: ask Mishania if this is ok.
    # Mind: __str__ uses colons, but Mishania's __repr__ use '=' chars
    def __repr__(self) -> str:
        return 'SeqTaxonomy(\n{}\n)'.format(self.__str__())
    # end def
# end class


def _str_None_rep(sth, None_rep : str = '') -> str:
    # It's a wrapper for str function,
    #     but is handles None is a special way
    return None_rep if sth is None else str(sth)
# end def
