
from src.util.strings import str_None_rep

class AlignResult:

    __slots__ = (
        'query_id',
        'hit_name',
        'hit_accession',
        'query_length',
        'alignment_length',
        'identity',
        'gaps',
        'evalue',
        'avg_quality',
        'accuracy',
    )

    def __init__(self,
                 query_id : str,
                 hit_name : str,
                 hit_accession : str,
                 query_length : int,
                 alignment_length: int,
                 identity : float,
                 gaps : int,
                 evalue : float,
                 avg_quality: float = None,
                 accuracy: float = None):
        self.query_id         = query_id
        self.hit_name         = hit_name
        self.hit_accession    = hit_accession
        self.query_length     = query_length
        self.alignment_length = alignment_length
        self.identity         = identity
        self.gaps             = gaps
        self.evalue           = evalue
        self.avg_quality      = avg_quality
        self.accuracy         = accuracy
    # end def

    def __str__(self):
        return f'''
query_id:         {self.query_id},
hit_name:         {self.hit_name},
hit_accession:    {self.hit_accession},
query_length:     {self.query_length},
alignment_length: {self.alignment_length},
identity:         {self.identity},
gaps:             {self.gaps},
evalue:           {self.evalue},
avg_quality:      {self.avg_quality},
accuracy:         {self.accuracy}.\n'''
    # end def

    def __repr__(self):
        return f'''AlignResult(
    query_id={self.query_id!r},
    hit_name={self.hit_name!r},
    hit_accession={self.hit_accession!r},
    query_length={self.query_length!r},
    alignment_length={self.alignment_length!r},
    identity={self.identity!r},
    gaps={self.gaps!r},
    evalue={self.evalue!r},
    avg_quality={self.avg_quality!r},
    accuracy={self.accuracy!r}
)'''
    # end def

    def to_tsv_row(self) -> str:
        sep ='\t'
        values = map(
            str_None_rep,
            (
                self.query_id,
                self.hit_name,
                self.hit_accession,
                self.query_length,
                self.alignment_length,
                self.identity,
                self.gaps,
                self.evalue,
                self.avg_quality,
                self.accuracy,
            )
        )
        return '{}\n'.format(sep.join(values))
    # end def
# end class
