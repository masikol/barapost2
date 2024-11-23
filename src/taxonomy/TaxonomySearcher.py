
import json
from xml.etree import ElementTree

from src.containers.SeqTaxonomy import SeqTaxonomy
from src.network.insistent_https_get import insistent_https_get
from src.taxonomy.taxonomy_config import RANKS_SORTED_DESCENDING


class TaxonomySearcher:

    def seach_taxonomy(self, accession_number: str) -> SeqTaxonomy:
        tax_id = self._acc2tax_id(accession_number)
        taxonomy = self._tax_id2taxonomy(tax_id, accession_number)
        return taxonomy
    # end def


    def _acc2tax_id(self, accession_number : str) -> int:
        elink_response = insistent_https_get(
            server='eutils.ncbi.nlm.nih.gov',
            server_path='/entrez/eutils/elink.fcgi',
            args= {
                'dbfrom'  : 'nuccore',
                'db'      : 'taxonomy',
                'id'      : accession_number,
                'retmode' : 'json',
            },
            request_for='Elink page to taxonomy db from nucore using an accession number',
            accession_number=accession_number
        )
        tax_id = self._parse_taxid(elink_response)
        return tax_id
    # end def

    def _parse_taxid(self, elink_response : str) -> str:
        # Example of an elink_response:
        # {
        # "header":{"type":"elink","version":"0.3"},
        # "linksets":[
        #     {
        #         "dbfrom":"nuccore",
        #         "ids":["1910759551"],
        #         "linksetdbs":[
        #             {
        #                  "dbto":"taxonomy",
        #                  "linkname":"nuccore_taxonomy",
        #                  "links":["930166"]
        # //                        ~~~~~~~~
        # //                        ^ we need this
        #             }
        #         ]
        #     }
        # ]
        # }
        # TODO: catch whatever json.loads raises
        response_dict = json.loads(elink_response)
        # TODO: catch KeyError, out of bounds error
        tax_ids = response_dict['linksets'][0]['linksetdbs'][0]['links']
        # TODO: if len(tax_ids) == 0
        return next(iter(tax_ids))
    # end def


    def _tax_id2taxonomy(self,
                         tax_id : str,
                         accession_number : str) -> SeqTaxonomy:
        esummary_response = insistent_https_get(
            server='eutils.ncbi.nlm.nih.gov',
            server_path='/entrez/eutils/efetch.fcgi',
            args= {
                'db'      : 'taxonomy',
                'id'      : tax_id,
                'retmode' : 'xml',
            },
            request_for='Esummary page of the taxonomy db for taxid `{}`'.format(tax_id),
        )
        taxonomy = self._parse_taxonomy(esummary_response, accession_number)
        return taxonomy
    # end def

    def _parse_taxonomy(self,
                        esummary_response : str,
                        accession_number : str) -> SeqTaxonomy:
        # Example of a response XML:
        #   https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=taxonomy&id=930166&retmode=xml
        # TODO: handle xml parsing errors
        root = ElementTree.fromstring(esummary_response)
        tax_name = root.findall('./Taxon/ScientificName')[0].text.strip()
        requested_taxon_rank = root.findall('./Taxon/Rank')[0].text.strip()

        tax_dict = {
            rank: None for rank in self._make_all_ncbi_ranks()
        }
        tax_dict[requested_taxon_rank] = tax_name
        taxon_elements = root.findall('./Taxon/LineageEx/Taxon')
        for tax_elem in taxon_elements:
            rank = tax_elem.findall('./Rank')[0].text.strip()
            if rank in tax_dict:
                tax_dict[rank] = tax_elem.findall('./ScientificName')[0].text.strip()
            # end if
        # end for

        if requested_taxon_rank == 'superkingdom':
            requested_taxon_rank = 'domain'
        # end if

        seq_taxonomy = SeqTaxonomy(
            seq_id=accession_number,
            rank=requested_taxon_rank.capitalize(),
            tax_name=tax_name,
            Domain=tax_dict['superkingdom'],
            Phylum=tax_dict['phylum'],
            Class=tax_dict['class'],
            Order=tax_dict['order'],
            Family=tax_dict['family'],
            Genus=tax_dict['genus'],
            Species=tax_dict['species']
        )
        return seq_taxonomy
    # end def

    def _make_all_ncbi_ranks(self):
        ranks = list(reversed(RANKS_SORTED_DESCENDING))
        # Replace the last one with 'superkingdom',
        #   because domain is named superkingdom in NCBI taxonomy
        ranks[-1] = 'superkingdom'
        # Make all of them lowercase for simplicity
        return list(
            map(
                lambda x: x.lower(),
                ranks
            )
        )
    # end def
# end class
