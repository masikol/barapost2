
import os
import glob
import shutil

import pytest

from src.hits.HitManager import HitManager
from src.containers.HitToDownload import HitToDownload
from src.config.hits import DB_FILE_NAME, SEP, COMMENT_CHAR


SOME_ACCESSION = 'NC_045512.2'
SOME_RECORD_NAME = 'Severe acute respiratory syndrome coronavirus 2 isolate Wuhan-Hu-1, complete genome'


# >>> Fixtures >>>

@pytest.fixture
def empty_classif_dir_path() -> str:
    dirpath = os.path.join(
        os.path.dirname(__file__),
        'test_data',
        'empty_classif_dir'
    )
    if not os.path.isdir(dirpath):
        os.makedirs(dirpath)
    # end if
    return dirpath
# end def

@pytest.fixture
def non_empty_classif_dir_path() -> str:
    dirpath = os.path.join(
        os.path.dirname(__file__),
        'test_data',
        'non_empty_classif_dir'
    )
    return dirpath
# end def

@pytest.fixture
def tmp_classif_dir_path() -> str:
    dirpath = os.path.join(
        os.path.dirname(__file__),
        'test_data',
        'tmp_classif_dir'
    )
    if not os.path.isdir(dirpath):
        os.makedirs(dirpath)
    # end if
    return dirpath
# end def


@pytest.fixture
def some_hit() -> HitToDownload:
    return HitToDownload(
        accession=SOME_ACCESSION,
        record_name=SOME_RECORD_NAME
    )
# end def

# <<< Fixtures <<<


# >>> Auxiliary function >>>

def empty_dir(dir_path : str):
    for path in glob.iglob(os.path.join(dir_path, '*')):
        if os.path.isfile(path):
            os.unlink(path)
        elif os.path.isdir(path):
            shitil.rmtree(path)
        else:
            assert False, 'Cannot remove file. Invalid type: {}'.format(path)
        # end if
    # end for
# end def

# <<< Auxiliary function <<<



class TestHitManager:

    def test_init_db(self, tmp_classif_dir_path : str):
        empty_dir(tmp_classif_dir_path)
        hit_manager = HitManager(tmp_classif_dir_path)
        assert type(hit_manager.hit_dict) == dict
        assert len(hit_manager.hit_dict) == 0
    # end def

    def test_read_empty_db(self, empty_classif_dir_path : str):
        hit_manager = HitManager(empty_classif_dir_path)
        assert type(hit_manager.hit_dict) == dict
        assert len(hit_manager.hit_dict) == 0
    # end def

    def test_read_non_empty_db(self, non_empty_classif_dir_path : str):
        hit_manager = HitManager(non_empty_classif_dir_path)

        assert type(hit_manager.hit_dict) == dict
        assert len(hit_manager.hit_dict) != 0

        for hit_accession, hit in hit_manager.hit_dict.items():
            assert type(hit_accession) == str
            assert type(hit) == HitToDownload
            assert type(hit.accession) == str
            assert hit.accession != ''
            assert type(hit.record_name) == str
            assert hit.record_name != ''
            assert type(hit.hit_count) == int
            assert hit.hit_count >= 0
            assert type(hit.replicons_checked) == bool
        # end for
    # end def

    def test_add_hit(self,
                     non_empty_classif_dir_path : str,
                     some_hit : HitToDownload):
        hit_manager = HitManager(non_empty_classif_dir_path)
        assert not some_hit.accession in hit_manager.hit_dict.keys(), \
            'Invalid fixture: some_hit.accession is in hit_manager.hit_dict.keys()'

        before_len = len(hit_manager.hit_dict)
        before_keys = frozenset(
            hit_manager.hit_dict.keys()
        )

        hit_manager.add_hit(some_hit)

        after_len = len(hit_manager.hit_dict)
        after_keys = frozenset(
            hit_manager.hit_dict.keys()
        )

        assert after_len == before_len + 1
        assert after_keys == before_keys | frozenset((some_hit.accession,))
    # end def


    def test_increment_hit(self, non_empty_classif_dir_path : str):
        hit_manager = HitManager(non_empty_classif_dir_path)
        some_accession = next(
            iter(
                hit_manager.hit_dict.keys()
            )
        )
        before_count = hit_manager.hit_dict[some_accession].hit_count
        inc_value = 4
        expected = before_count + inc_value

        hit_manager.increment_hit(some_accession, inc_value)

        observed = hit_manager.hit_dict[some_accession].hit_count

        assert observed == expected
    # end def

    def test_increment_hit_default(self, non_empty_classif_dir_path : str):
        hit_manager = HitManager(non_empty_classif_dir_path)
        some_accession = next(
            iter(
                hit_manager.hit_dict.keys()
            )
        )
        before_count = hit_manager.hit_dict[some_accession].hit_count
        expected = before_count + 1

        hit_manager.increment_hit(some_accession)

        observed = hit_manager.hit_dict[some_accession].hit_count

        assert observed == expected
    # end def


    def test_basic_io(self,
                      non_empty_classif_dir_path : str):
        hit_manager = HitManager(non_empty_classif_dir_path)
        expected = hit_manager.hit_dict

        hit_manager.rewrite_db()
        hit_manager = HitManager(non_empty_classif_dir_path)
        observed = hit_manager.hit_dict

        assert type(expected) == type(observed)
        assert len(expected) == len(observed)
        assert(
            frozenset(expected.keys()) == frozenset(observed.keys())
        )
    # end def
# end class
