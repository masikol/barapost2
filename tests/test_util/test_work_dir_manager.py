
import os
import re
import glob
import shutil
from typing import Sequence

import pytest

from src.containers.Fasta import Fasta
from src.containers.HTSRecord import HTSRecord
from src.util.BarapostWorkDirManager import BarapostWorkDirManager


# >>> Fixtures >>>

@pytest.fixture
def some_workdir() -> str:
    return os.path.join(
        os.path.dirname(__file__),
        'data',
        'test_workdir'
    )
# end def

@pytest.fixture
def some_fasta_fpath() -> str:
    return os.path.join(
        os.path.dirname(__file__),
        'hot_seqs.fasta'
    )
# end def

@pytest.fixture
def another_fasta_fpath() -> str:
    return os.path.join(
        '{}_2'.format(os.path.dirname(__file__)),
        'hot_seqs.fasta'
    )
# end def

@pytest.fixture
def yet_another_fasta_fpath() -> str:
    return os.path.join(
        os.path.dirname(__file__),
        'hard_seqs.fasta'
    )
# end def


@pytest.fixture
def intact_workdir_path() -> str:
    return os.path.join(
        os.path.dirname(__file__),
        'data',
        'intact_workdir'
    )
# end def

@pytest.fixture
def intact_workdir_copy_path() -> str:
    return os.path.join(
        os.path.dirname(__file__),
        'data',
        'intact_workdir_copy'
    )
# end def

@pytest.fixture
def input_hts_fpath_1() -> str:
    # The path is intentionally hardcoded so that
    #   the test will work on Windows
    return '/tmp/query_corona_seq.fasta'
# end def

@pytest.fixture
def input_hts_fpath_2() -> str:
    # The path is intentionally hardcoded so that
    #   the test will work on Windows
    return '/tmp/some_seqs.fastq.gz'
# end def


@pytest.fixture
def some_fasta_packet() -> Sequence[Fasta]:
    return (
        Fasta('hot_seqs_1', 'CATGCTGATGCGAGTTGCAC'),
        Fasta('hot_seqs_2', 'ACTATGCTGATCGAGTCGTAGTC'),
    )
# end def


@pytest.fixture
def some_request_id() -> str:
    return 'RUH38726876'
# end def

# <<< Fixtures <<<


class TestWorkDirManager:

    def test_make_classification_dir_path(self, some_workdir : str):
        manager = BarapostWorkDirManager(some_workdir)
        expected = os.path.join(some_workdir, 'classification')
        observed = manager.make_classification_dir_path()
        assert observed == expected
    # end def

    def test_make_tmp_dir_path(self, some_workdir : str):
        manager = BarapostWorkDirManager(some_workdir)
        expected = os.path.join(some_workdir, 'tmp')
        observed = manager.make_tmp_dir_path()
        assert observed == expected
    # end def

    def test_subdirs_exist(self, some_workdir : str):
        manager = BarapostWorkDirManager(some_workdir)
        assert os.path.isdir(some_workdir)
        assert os.path.isdir(manager.make_classification_dir_path())
        assert os.path.isdir(manager.make_tmp_dir_path())
    # end def


    def test_make_classif_fpath_ident_paths(self,
                                            some_workdir : str,
                                            some_fasta_fpath : str):
        manager = BarapostWorkDirManager(some_workdir)
        path_1 = manager.make_classification_fpath(some_fasta_fpath)
        path_2 = manager.make_classification_fpath(some_fasta_fpath)
        assert path_1 == path_2
    # end def

    def test_make_classif_fpath_ident_basenames(self,
                                                some_workdir : str,
                                                some_fasta_fpath : str,
                                                another_fasta_fpath : str):
        manager = BarapostWorkDirManager(some_workdir)
        path_1 = manager.make_classification_fpath(some_fasta_fpath)
        path_2 = manager.make_classification_fpath(another_fasta_fpath)
        assert path_1 != path_2
    # end def

    def test_make_classif_fpath_different_paths(self,
                                                some_workdir : str,
                                                some_fasta_fpath : str,
                                                yet_another_fasta_fpath : str):
        manager = BarapostWorkDirManager(some_workdir)
        path_1 = manager.make_classification_fpath(some_fasta_fpath)
        path_2 = manager.make_classification_fpath(yet_another_fasta_fpath)
        assert path_1 != path_2
    # end def


    def test_make_tmp_blast_fpath_ident_paths(self,
                                              some_workdir : str,
                                              some_fasta_fpath : str):
        manager = BarapostWorkDirManager(some_workdir)
        path_1 = manager.make_tmp_remote_blast_fpath(some_fasta_fpath)
        path_2 = manager.make_tmp_remote_blast_fpath(some_fasta_fpath)
        assert path_1 == path_2
    # end def

    def test_make_tmp_blast_fpath_ident_basenames(self,
                                                  some_workdir : str,
                                                  some_fasta_fpath : str,
                                                  another_fasta_fpath : str):
        manager = BarapostWorkDirManager(some_workdir)
        path_1 = manager.make_tmp_remote_blast_fpath(some_fasta_fpath)
        path_2 = manager.make_tmp_remote_blast_fpath(another_fasta_fpath)
        assert path_1 != path_2
    # end def

    def test_make_tmp_blast_fpath_different_paths(self,
                                                  some_workdir : str,
                                                  some_fasta_fpath : str,
                                                  yet_another_fasta_fpath : str):
        manager = BarapostWorkDirManager(some_workdir)
        path_1 = manager.make_tmp_remote_blast_fpath(some_fasta_fpath)
        path_2 = manager.make_tmp_remote_blast_fpath(yet_another_fasta_fpath)
        assert path_1 != path_2
    # end def



    def test_count_classif_records_nary(self,
                                        intact_workdir_path : str):
        # "Nary" means no records in the classification file
        manager = BarapostWorkDirManager(intact_workdir_path)
        random_path = '/How/odd/to/watch/a/mortal/kindle'
        expected_record_count = 0
        observed_record_count = manager.count_classification_records(
            random_path
        )
        assert observed_record_count == expected_record_count
    # end def

    def test_count_classif_records_single(self,
                                          intact_workdir_path : str,
                                          input_hts_fpath_1 : str):
        # "Single" means single record in the classification file
        manager = BarapostWorkDirManager(intact_workdir_path)
        expected_record_count = 1
        observed_record_count = manager.count_classification_records(
            input_hts_fpath_1
        )
        assert observed_record_count == expected_record_count
    # end def

    def test_count_classif_records_multiple(self,
                                            intact_workdir_path : str,
                                            input_hts_fpath_2 : str):
        # "Single" means single record in the classification file
        manager = BarapostWorkDirManager(intact_workdir_path)
        expected_record_count = 7
        observed_record_count = manager.count_classification_records(
            input_hts_fpath_2
        )
        assert observed_record_count == expected_record_count
    # end def


    def test_empty_old_run_dirs(self,
                                intact_workdir_path : str,
                                intact_workdir_copy_path : str):
        if os.path.isdir(intact_workdir_copy_path):
            shutil.rmtree(intact_workdir_copy_path)
        # end if
        shutil.copytree(intact_workdir_path, intact_workdir_copy_path)

        manager = BarapostWorkDirManager(intact_workdir_copy_path)
        manager.empty_old_run_dirs()

        num_files_classif_dir = len(glob.glob(
            os.path.join(
                manager.make_classification_dir_path(), '*'
            )
        ))
        assert num_files_classif_dir == 0

        num_files_tmp_dir = len(glob.glob(
            os.path.join(
                manager.make_tmp_dir_path(), '*'
            )
        ))
        assert num_files_tmp_dir == 0

        shutil.rmtree(intact_workdir_copy_path)
    # end def


    def test_rm_tmp_remote_blast_file(self,
                                      intact_workdir_path : str,
                                      intact_workdir_copy_path : str,
                                      input_hts_fpath_1 : str):
        if os.path.isdir(intact_workdir_copy_path):
            shutil.rmtree(intact_workdir_copy_path)
        # end if
        shutil.copytree(intact_workdir_path, intact_workdir_copy_path)

        manager = BarapostWorkDirManager(intact_workdir_copy_path)
        tmp_file_path = manager.make_tmp_remote_blast_fpath(input_hts_fpath_1)

        manager.rm_tmp_remote_blast_file(input_hts_fpath_1)

        assert not os.path.isfile(tmp_file_path)

        shutil.rmtree(intact_workdir_copy_path)
    # end def

    def test_write_tmp_remote_blast_file(self,
                                    intact_workdir_path : str,
                                    intact_workdir_copy_path : str,
                                    input_hts_fpath_1 : str,
                                    some_fasta_packet : Sequence[Fasta],
                                    some_request_id : str):
        if os.path.isdir(intact_workdir_copy_path):
            shutil.rmtree(intact_workdir_copy_path)
        # end if
        shutil.copytree(intact_workdir_path, intact_workdir_copy_path)

        manager = BarapostWorkDirManager(intact_workdir_copy_path)
        manager.write_tmp_remote_blast_file(
            some_request_id,
            input_hts_fpath_1,
            some_fasta_packet
        )
        tmp_file_path = manager.make_tmp_remote_blast_fpath(input_hts_fpath_1)

        assert os.path.isfile(tmp_file_path)

        shutil.rmtree(intact_workdir_copy_path)
    # end def

    def test_load_nonextant_tmp_remote_blast_file(self,
                                                  intact_workdir_path : str,
                                                  intact_workdir_copy_path : str,
                                                  input_hts_fpath_1 : str):
        if os.path.isdir(intact_workdir_copy_path):
            shutil.rmtree(intact_workdir_copy_path)
        # end if
        shutil.copytree(intact_workdir_path, intact_workdir_copy_path)

        missing_hts_fpath = '{}_ODD'.format(input_hts_fpath_1)

        manager = BarapostWorkDirManager(intact_workdir_copy_path)

        tmp_data = manager.load_tmp_remote_blast_file(missing_hts_fpath)

        assert tmp_data is None

        shutil.rmtree(intact_workdir_copy_path)
    # end def

    def test_load_extant_tmp_remote_blast_file(self,
                                               intact_workdir_path : str,
                                               intact_workdir_copy_path : str,
                                               input_hts_fpath_1 : str):
        if os.path.isdir(intact_workdir_copy_path):
            shutil.rmtree(intact_workdir_copy_path)
        # end if
        shutil.copytree(intact_workdir_path, intact_workdir_copy_path)

        manager = BarapostWorkDirManager(intact_workdir_copy_path)

        tmp_data = manager.load_tmp_remote_blast_file(input_hts_fpath_1)

        assert not tmp_data is None
        assert 'fpath' in tmp_data.keys()
        assert 'request_id' in tmp_data.keys()
        assert 'packet_size' in tmp_data.keys()
        assert 'quality_dict' in tmp_data.keys()

        shutil.rmtree(intact_workdir_copy_path)
    # end def


    def test_make_classif_archive_dirpath(self,
                                          intact_workdir_path : str,
                                          intact_workdir_copy_path : str):
        if os.path.isdir(intact_workdir_copy_path):
            shutil.rmtree(intact_workdir_copy_path)
        # end if
        shutil.copytree(intact_workdir_path, intact_workdir_copy_path)

        manager = BarapostWorkDirManager(intact_workdir_copy_path)
        archive_dirpath = manager.make_classif_archive_dirpath()

        assert type(archive_dirpath) == str
        assert os.path.dirname(archive_dirpath) == intact_workdir_copy_path
        assert re.match(
            r'classification_archive_[0-9]+',
            os.path.basename(archive_dirpath)
        )

        shutil.rmtree(intact_workdir_copy_path)
    # end def


    def test_archive_classification_dir(self,
                                        intact_workdir_path : str,
                                        intact_workdir_copy_path : str):
        if os.path.isdir(intact_workdir_copy_path):
            shutil.rmtree(intact_workdir_copy_path)
        # end if
        shutil.copytree(intact_workdir_path, intact_workdir_copy_path)

        manager = BarapostWorkDirManager(intact_workdir_copy_path)
        archive_dirpath = manager.archive_classification_dir()

        assert os.path.isdir(archive_dirpath)

        total_num_files_in_archive = len(glob.glob(
            os.path.join(archive_dirpath, '*')
        ))
        num_gz_files_in_archive = len(glob.glob(
            os.path.join(archive_dirpath, '*.gz')
        ))
        only_gzipped_files = total_num_files_in_archive == num_gz_files_in_archive
        assert only_gzipped_files

        num_tmp_files = len(
            glob.glob(
                os.path.join(manager.make_tmp_dir_path(), '*')
            )
        )
        assert num_tmp_files == 0

        shutil.rmtree(intact_workdir_copy_path)
    # end def

# end class
