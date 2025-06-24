
RANKS_SORTED_DESCENDING = [
    'Domain',
    'Phylum',
    'Class',
    'Order',
    'Family',
    'Genus',
    'Species',
]

TAXONOMY_SEP = '\t'
COMMENT_CHAR = '#'

# All rank names start with a capital letter
#     because 'class' is a Python keyword.
TAXONOMY_COLNAMES = (
    'seq_id',
    'rank',
    'tax_name',
    'Domain',
    'Phylum',
    'Class',
    'Order',
    'Family',
    'Genus',
    'Species',
)


# A pattern for matching name of any rank except species:
HIGH_TAX_NAME_PATT = r"[A-Z][a-z\.]+"
# A pattern to match species name
SPECIES_PATT = r"[A-Za-z0-9\._]+"
# A separator for user-supplied taxonomy string
OWN_SEQ_TAX_SEP = ';'
# A pattern for matching whole taxonomy string of a user-supplied taxonomy string.
# 6 semisolons with probable absence of name ending with species name.
# All without spaces.
OWN_SEQ_TAXONOMY_FMT = r"(((%s)?%s){6}(%s)?)" % (HIGH_TAX_NAME_PATT, OWN_SEQ_TAX_SEP, SPECIES_PATT)

# The name of a taxonomy file in barapost work dir
DB_FILE_NAME = 'taxonomy.tsv'

# Maximum number of attempts to search taxonomy
MAX_SEARCH_ATTEMPT_COUNT = 3
