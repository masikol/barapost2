
import os
import glob
import shutil

import pytest

from src.containers.AlignResult import AlignResult
from src.seq_db.SeqDbListManager import SeqDbListManager
from src.containers.SeqDbListRecord import SeqDbListRecord
from src.config.seq_db import DB_FILE_NAME, SEP, COMMENT_CHAR


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
def some_align_result() -> AlignResult:
    return AlignResult(
        query_id='query_seq',
        hit_name=SOME_RECORD_NAME,
        hit_accession=SOME_ACCESSION,
        query_length=1000,
        alignment_length=1000,
        identity=999,
        gaps=0,
        evalue=0.0,
        avg_quality=6.8,
        accuracy=98.7
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



class TestSeqDbListManager:

    def test_init_db(self, tmp_classif_dir_path : str):
        empty_dir(tmp_classif_dir_path)
        manager = SeqDbListManager(tmp_classif_dir_path)
        assert type(manager.seq_db_dict) == dict
        assert len(manager.seq_db_dict) == 0
    # end def

    def test_read_empty_db(self, empty_classif_dir_path : str):
        manager = SeqDbListManager(empty_classif_dir_path)
        assert type(manager.seq_db_dict) == dict
        assert len(manager.seq_db_dict) == 0
    # end def

    def test_read_non_empty_db(self, non_empty_classif_dir_path : str):
        manager = SeqDbListManager(non_empty_classif_dir_path)

        assert type(manager.seq_db_dict) == dict
        assert len(manager.seq_db_dict) != 0

        for hit_accession, hit in manager.seq_db_dict.items():
            assert type(hit_accession) == str
            assert type(hit) == SeqDbListRecord
            assert type(hit.accession) == str
            assert hit.accession != ''
            assert type(hit.record_name) == str
            assert hit.record_name != ''
            assert type(hit.hit_count) == int
            assert hit.hit_count >= 0
            assert type(hit.replicons_checked) == bool
        # end for
    # end def

    def test_add_seq_db_record(self,
                     non_empty_classif_dir_path : str,
                     some_align_result : AlignResult):
        manager = SeqDbListManager(non_empty_classif_dir_path)
        assert not some_align_result.hit_accession in manager.seq_db_dict.keys(), \
            'Invalid fixture: some_align_result.hit_accession is in manager.seq_db_dict.keys()'

        before_len = len(manager.seq_db_dict)
        before_keys = frozenset(
            manager.seq_db_dict.keys()
        )

        manager.add_seq_db_record(some_align_result)

        after_len = len(manager.seq_db_dict)
        after_keys = frozenset(
            manager.seq_db_dict.keys()
        )

        assert after_len == before_len + 1
        assert after_keys == before_keys | frozenset((some_align_result.hit_accession,))

    # end def


    def test_increment_hit(self, non_empty_classif_dir_path : str):
        manager = SeqDbListManager(non_empty_classif_dir_path)
        some_accession = next(
            iter(
                manager.seq_db_dict.keys()
            )
        )
        before_count = manager.seq_db_dict[some_accession].hit_count
        inc_value = 4
        expected = before_count + inc_value

        manager._increment_hit(some_accession, inc_value)

        observed = manager.seq_db_dict[some_accession].hit_count

        assert observed == expected
    # end def

    def test_increment_hit_default(self, non_empty_classif_dir_path : str):
        manager = SeqDbListManager(non_empty_classif_dir_path)
        some_accession = next(
            iter(
                manager.seq_db_dict.keys()
            )
        )
        before_count = manager.seq_db_dict[some_accession].hit_count
        expected = before_count + 1

        manager._increment_hit(some_accession)

        observed = manager.seq_db_dict[some_accession].hit_count

        assert observed == expected
    # end def


    def test_increment_hit_new_hit(self,
                                   non_empty_classif_dir_path : str,
                                   some_align_result : AlignResult):
        manager = SeqDbListManager(non_empty_classif_dir_path)
        assert not some_align_result.hit_accession in manager.seq_db_dict.keys(), \
            'Invalid fixture: some_align_result.hit_accession is in manager.seq_db_dict.keys()'

        manager.add_seq_db_record(some_align_result)

        hit = manager.seq_db_dict[some_align_result.hit_accession]
        assert hit.hit_count == 1
    # end def


    def test_basic_io(self,
                      non_empty_classif_dir_path : str):
        manager = SeqDbListManager(non_empty_classif_dir_path)
        expected = manager.seq_db_dict

        manager.rewrite_db()
        manager = SeqDbListManager(non_empty_classif_dir_path)
        observed = manager.seq_db_dict

        assert type(expected) == type(observed)
        assert len(expected) == len(observed)
        assert(
            frozenset(expected.keys()) == frozenset(observed.keys())
        )
    # end def
# end class
