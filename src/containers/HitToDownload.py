
import sys

from src.config.hits import SEP
from src.util.strings import str_None_rep
from src.containers.AlignResult import AlignResult


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

        replicons_checked = True if split_row[3].strip() == '1' else False

        try:
            hits_count = int(split_row[2].strip())
            if hits_count < 0:
                raise ValueError
            # end if
        except ValueError as err:
            logging.critical(
                'Error: cannot parse hit count for the line with accession {}' \
                    .format(split_row[0])
            )
            logging.critical(str(err))
            sys.exit(1)
        # end try

        return HitToDownload(
            accession=split_row[0].strip(),
            record_name=split_row[1].strip(),
            hit_count=hits_count,
            replicons_checked=replicons_checked
        )
    # end def


    # TODO: test
    @classmethod
    def from_align_result(cls,
                          align_result : AlignResult) -> 'HitToDownload':
        return HitToDownload(
            accession=align_result.hit_accession,
            record_name=align_result.hit_name,
            hit_count=1,
            replicons_checked=False
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
