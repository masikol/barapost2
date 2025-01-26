
from src.config.hits import SEP
from src.util.strings import str_None_rep


class HitToDownload:

    __slots__ = (
        'accession',
        'record_name',
        'hit_count',
        'replicons_checked',
    )


    def __init__(self,
                 accession : str,
                 record_name : str,
                 hit_count : int = 0,
                 replicons_checked : bool = False):
        self.accession         = accession
        self.record_name       = record_name
        self.hit_count         = hit_count
        self.replicons_checked = replicons_checked
    # end def


    def increment(self, value : int = 1):
        self.hit_count += value
    # end def


    def to_tsv_row(self) -> str:
        values = map(
            str_None_rep,
            (
                self.accession,
                self.record_name,
                self.hit_count,
                '1' if self.replicons_checked else '0',
            )
        )
        return '{}\n'.format(SEP.join(values))
    # end def


    @classmethod
    def from_tsv_row(cls,
                     row_str : str,
                     sep : str = SEP) -> 'HitToDownload':
        split_row = tuple(
            map(
                str.strip,
                row_str.split(sep)
            )
        )
        replicons_checked = True if split_row[3] == '1' else False
        return HitToDownload(
            accession=split_row[0],
            record_name=split_row[1],
            hit_count=int(split_row[2]), # TODO: validate int, because db is free to edit by users
            replicons_checked=replicons_checked
        )
    # end def


    def __eq__(self, other : object) -> bool:
        return type(self)             == type(other) \
           and self.accession         == other.accession \
           and self.record_name       == other.record_name \
           and self.hit_count         == other.hit_count \
           and self.replicons_checked == other.replicons_checked
    # end def


    def __str__(self) -> str:
        return f'''
accession:         {self.accession},
record_name:       {self.record_name},
hit_count:         {self.hit_count},
replicons_checked: {self.replicons_checked}.\n'''
    # end def

    def __repr__(self) -> str:
        return f'''HitToDownload(
    accession={self.accession!r},
    record_name={self.record_name!r},
    hit_count={self.hit_count!r},
    replicons_checked={self.replicons_checked!r}
)'''
    # end def
# end class
