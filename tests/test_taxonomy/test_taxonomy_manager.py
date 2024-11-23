
import os

import pytest

from src.filesystem import remove_bad_chars
from src.containers.SeqTaxonomy import SeqTaxonomy
from src.taxonomy.TaxonomyManager import TaxonomyManager


# === Fixtures ===

@pytest.fixture
def accession_number_1() -> str:
    return 'CP045701.2' # GenBank
# end def


@pytest.fixture
def own_seq_haystack_str_1() -> str:
    return 'SOMETHINS_BEFORE ' \
           'Bacteria;Pseudomonadota;Gammaproteobacteria;Pseudomonadales;' \
           'Pseudomonadaceae;Pseudomonas;Pseudomonas_brassicacearum' \
           ' SOMETHING AFTER'
# end def

@pytest.fixture
def own_seq_haystack_str_2() -> str:
    return remove_bad_chars('some pseudomonas, Im not sure')
# end def


# === Test classes ===

class TestTaxonomyManager:

    def test_basic_accession(self, accession_number_1):
        tmp_tax_fpath = self._get_tmp_tax_fpath()
        with open(tmp_tax_fpath, 'wt') as out_handle:
            pass
        # end with
        expected = SeqTaxonomy(
            seq_id=accession_number_1,
            rank='Species',
            tax_name='Pseudomonas brassicacearum',
            Domain='Bacteria',
            Phylum='Pseudomonadota',
            Class='Gammaproteobacteria',
            Order='Pseudomonadales',
            Family='Pseudomonadaceae',
            Genus='Pseudomonas',
            Species='Pseudomonas brassicacearum'
        )

        taxonomy_manager = TaxonomyManager(tmp_tax_fpath)
        taxonomy_manager.add_taxonomy(accession_number_1)
        observed = SeqTaxonomy.from_tsv_row(
            self._get_first_data_line(tmp_tax_fpath)
        )

        assert observed == expected
    # end def


    def test_parse_own_seq_taxonomy_1(self, accession_number_1, own_seq_haystack_str_1):
        tmp_tax_fpath = self._get_tmp_tax_fpath()
        with open(tmp_tax_fpath, 'wt') as out_handle:
            pass
        # end with
        expected = SeqTaxonomy(
            seq_id=accession_number_1,
            rank='Species',
            tax_name='Pseudomonas_brassicacearum',
            Domain='Bacteria',
            Phylum='Pseudomonadota',
            Class='Gammaproteobacteria',
            Order='Pseudomonadales',
            Family='Pseudomonadaceae',
            Genus='Pseudomonas',
            Species='Pseudomonas_brassicacearum'
        )

        taxonomy_manager = TaxonomyManager(tmp_tax_fpath)
        observed = taxonomy_manager.parse_own_seq_taxonomy(
            accession_number_1,
            own_seq_haystack_str_1
        )

        assert observed == expected
    # end def

    def test_parse_own_seq_taxonomy_2(self, accession_number_1, own_seq_haystack_str_2):
        tmp_tax_fpath = self._get_tmp_tax_fpath()
        with open(tmp_tax_fpath, 'wt') as out_handle:
            pass
        # end with
        expected = SeqTaxonomy(
            seq_id=accession_number_1,
            rank=None,
            tax_name=own_seq_haystack_str_2,
            Domain=None,
            Phylum=None,
            Class=None,
            Order=None,
            Family=None,
            Genus=None,
            Species=None
        )

        taxonomy_manager = TaxonomyManager(tmp_tax_fpath)
        observed = taxonomy_manager.parse_own_seq_taxonomy(
            accession_number_1,
            own_seq_haystack_str_2
        )

        assert observed == expected
    # end def


    def _get_tmp_tax_fpath(self) -> str:
        return os.path.join(
            os.path.dirname(__file__),
            'tmp_taxonomy.tsv'
        )
    # end def

    def _get_first_data_line(self, table_fpath: str) -> str:
        with open(table_fpath, 'rt') as in_handle:
            in_handle.readline() # pass header line
            first_data_line = in_handle.readline()
        # end def
        return first_data_line
    # end def
# end def
