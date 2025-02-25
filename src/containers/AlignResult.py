
from src.containers.Fastq import Q_to_pe
from src.util.strings import str_None_rep
from src.config.align_result import HIT_SEP
from src.util.simplify_read_id import simplify_read_id


SEP = '\t'


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
        self.query_id         = simplify_read_id(query_id)
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


    @classmethod
    def make_empty_result(cls,
                          query_id : str,
                          query_length = int) -> 'AlignResult':
        return AlignResult(
            query_id=simplify_read_id(query_id),
            hit_name=None,
            hit_accession=None,
            query_length=query_length,
            alignment_length=None,
            identity=None,
            gaps=None,
            evalue=None,
            avg_quality=None,
            accuracy=None
        )
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
        return '{}\n'.format(SEP.join(values))
    # end def


    def to_console_summary(self) -> str:
        sep = '\n#' + ' ' * 4
        if self.hit_accession is None:
            output_str = sep.join(
                (
                    '# {} -- No significant similarity found;'.format(
                        self.query_id
                    ),
                    'Query length - {};'.format(self.query_length),
                )
            )
        else:
            identity_ratio = round(
                float(self.identity) / int(self.alignment_length) * 100,
                2
            )
            gaps_ratio = round(
                float(self.gaps) / int(self.alignment_length) * 100,
                2
            )
            output_str = sep.join(
                (
                    '# {} -- {} {};'.format(
                        self.query_id,
                        self.hit_accession,
                        self.hit_name
                    ),
                    'Query length - {};'.format(self.query_length),
                    'Identity - {:.2f}/{} ({:.2f}%); Gaps - {}/{} ({:.2f}%);'.format(
                        self.identity, self.alignment_length, identity_ratio,
                        self.gaps, self.alignment_length, gaps_ratio,
                    )
                )
            )
        # end if

        if not self.avg_quality is None:
            output_str += sep \
                       + 'Average quality of the read is {:.2f}, i.e. accuracy is {}%;' \
                           .format(self.avg_quality, self.accuracy)
        # end if

        return '{}\n'.format(output_str)
    # end def


    @classmethod
    def get_header_str(cls) -> str:
        return SEP.join(
            AlignResult.__slots__,
        ) + '\n'
    # end def


    def add_query_quality(self, query_quality : float):
        self.avg_quality = query_quality
        if query_quality is None:
            self.accuracy = None
        else:
            self.accuracy = round(
                100.0 - (100.0 * Q_to_pe(query_quality)),
                2
            )
        # end if
    # end def


    @classmethod
    def merge(ar1 : 'AlignResult',
              ar2 : 'AlignResult') -> 'AlignResult':
        result_ar = ar1
        result_ar.hit_name += HIT_SEP + ar2.hit_name
        result_ar.hit_accession += HIT_SEP + ar2.hit_accession
        return result_ar
    # end def
# end class
