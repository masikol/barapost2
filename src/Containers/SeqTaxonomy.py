
class SeqTaxonomy:

    # All rank names start with a capital letter
    #     because 'class' is a Python keyword.
    __slots__ = (
        'seq_id',
        'rank',
        'tax_id',
        'tax_name',
        'Domain',
        'Phylum',
        'Class',
        'Order',
        'Family',
        'Genus',
        'Species',
    )

    def __init__(self,
                 seq_id   : str,
                 rank     : str,
                 tax_id   : int = None,
                 tax_name : str = None,
                 Domain   : str = None,
                 Phylum   : str = None,
                 Class    : str = None,
                 Order    : str = None,
                 Family   : str = None,
                 Genus    : str = None,
                 Species  : str = None):
        self.seq_id   = seq_id
        self.rank   = rank
        self.tax_id   = tax_id
        self.tax_name = tax_name
        self.Domain   = Domain
        self.Phylum   = Phylum
        self.Class    = Class
        self.Order    = Order
        self.Family   = Family
        self.Genus    = Genus
        self.Species  = Species
    # end def

    def to_tsv_row(self, sep : str = '\t') -> str:
        values = map(
            _str_None_rep,
            (
                self.seq_id,
                self.rank,
                self.tax_id,
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
        return sep.join(values)
    # end def

    def __str__(self):
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
                   self.tax_id,
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
    def __repr__(self):
        return 'SeqTaxonomy(\n{}\n)'.format(self.__str__())
    # end def
# end class


def _str_None_rep(sth, None_rep=''):
    # It's a wrapper for str function,
    #     but is handles None is a special way
    return None_rep if sth is None else str(sth)
# end def
