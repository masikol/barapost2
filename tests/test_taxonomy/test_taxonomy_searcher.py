
import pytest

from src.taxonomy.TaxonomySearcher import TaxonomySearcher


# === Fixtures ===

@pytest.fixture
def accession_number_1() -> str:
    return 'CP045701.2' # GenBank
# end def

@pytest.fixture
def accession_number_2() -> str:
    return 'NZ_CP045701.2' # RefSeq
# end def

@pytest.fixture
def accession_number_3() -> str:
    # A sequence with taxid 286, which is not at the species rank, but on the genus rank
    return 'MW857984.1'
# end def

@pytest.fixture
def accession_number_4() -> str:
    # A sequence with taxid 2, which is at the domain (aka superkingdom) rank
    return 'HH944705.1'
# end def


# === Test classes ===

class TestTaxonomySearcher:

    def test_case_1(self, accession_number_1):
        tax_searcher = TaxonomySearcher()
        seq_taxonomy = tax_searcher.seach_taxonomy(accession_number_1)
        assert seq_taxonomy.seq_id   == accession_number_1
        assert seq_taxonomy.rank     == 'Species'
        assert seq_taxonomy.tax_name == 'Pseudomonas brassicacearum'
        assert seq_taxonomy.Domain   == 'Bacteria'
        assert seq_taxonomy.Phylum   == 'Pseudomonadota'
        assert seq_taxonomy.Class    == 'Gammaproteobacteria'
        assert seq_taxonomy.Order    == 'Pseudomonadales'
        assert seq_taxonomy.Family   == 'Pseudomonadaceae'
        assert seq_taxonomy.Genus    == 'Pseudomonas'
        assert seq_taxonomy.Species  == 'Pseudomonas brassicacearum'
    # end def

    def test_case_2(self, accession_number_2):
        tax_searcher = TaxonomySearcher()
        seq_taxonomy = tax_searcher.seach_taxonomy(accession_number_2)
        assert seq_taxonomy.seq_id   == accession_number_2
        assert seq_taxonomy.rank     == 'Species'
        assert seq_taxonomy.tax_name == 'Pseudomonas brassicacearum'
        assert seq_taxonomy.Domain   == 'Bacteria'
        assert seq_taxonomy.Phylum   == 'Pseudomonadota'
        assert seq_taxonomy.Class    == 'Gammaproteobacteria'
        assert seq_taxonomy.Order    == 'Pseudomonadales'
        assert seq_taxonomy.Family   == 'Pseudomonadaceae'
        assert seq_taxonomy.Genus    == 'Pseudomonas'
        assert seq_taxonomy.Species  == 'Pseudomonas brassicacearum'
    # end def

    def test_case_3(self, accession_number_3):
        tax_searcher = TaxonomySearcher()
        seq_taxonomy = tax_searcher.seach_taxonomy(accession_number_3)
        assert seq_taxonomy.seq_id   == accession_number_3
        assert seq_taxonomy.rank     == 'Genus'
        assert seq_taxonomy.tax_name == 'Pseudomonas'
        assert seq_taxonomy.Domain   == 'Bacteria'
        assert seq_taxonomy.Phylum   == 'Pseudomonadota'
        assert seq_taxonomy.Class    == 'Gammaproteobacteria'
        assert seq_taxonomy.Order    == 'Pseudomonadales'
        assert seq_taxonomy.Family   == 'Pseudomonadaceae'
        assert seq_taxonomy.Genus    == 'Pseudomonas'
        assert seq_taxonomy.Species  == None
    # end def

    def test_case_4(self, accession_number_4):
        tax_searcher = TaxonomySearcher()
        seq_taxonomy = tax_searcher.seach_taxonomy(accession_number_4)
        assert seq_taxonomy.seq_id   == accession_number_4
        assert seq_taxonomy.rank     == 'Domain'
        assert seq_taxonomy.tax_name == 'Bacteria'
        assert seq_taxonomy.Domain   == 'Bacteria'
        assert seq_taxonomy.Phylum   == None
        assert seq_taxonomy.Class    == None
        assert seq_taxonomy.Order    == None
        assert seq_taxonomy.Family   == None
        assert seq_taxonomy.Genus    == None
        assert seq_taxonomy.Species  == None
    # end def
# end def
