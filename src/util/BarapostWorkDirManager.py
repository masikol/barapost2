
import os
import gzip
import json
import glob
import shutil
import logging
import hashlib
from typing import Sequence, TypeAlias

import src.filesystem as fs
from src.time import humane_time
from src.config.seq_db import DB_FILE_NAME as SEQDB_DB_FILE_NAME
from src.config.taxonomy import DB_FILE_NAME as TAX_DB_FILE_NAME
from src.containers.HTSRecord import HTSRecord
from src.config.classif_files import COMMENT_CHAR
from src.containers.AlignResult import AlignResult
from src.containers.Fastq import make_quality_dict


SeqPacket : TypeAlias = Sequence[HTSRecord]


class BarapostWorkDirManager:

    def __init__(self, work_dirpath : str):
        self.work_dirpath = os.path.abspath(
            work_dirpath
        )
        self._init_work_subdirs()
    # end def

    def _init_work_subdirs(self):
        dir_paths = (
            self.work_dirpath,
            self.make_classification_dir_path(),
            self.make_tmp_dir_path(),
        )
        for dir_path in dir_paths:
            if not os.path.isdir(dir_path):
                os.makedirs(dir_path)
            # end if
        # end for
    # end def


    def make_classification_dir_path(self) -> str:
        return os.path.join(
            self.work_dirpath,
            'classification'
        )
    # end def

    def make_tmp_dir_path(self) -> str:
        return os.path.join(
            self.work_dirpath,
            'tmp'
        )
    # end def

    def make_classification_fpath(self, input_hts_fpath : str) -> str:
        classif_hash = self.make_classif_hash(input_hts_fpath)
        return os.path.join(
            self.make_classification_dir_path(),
            '{}.tsv'.format(classif_hash)
        )
    # end def

    def make_classif_hash(self, input_hts_fpath : str) -> str:
        return hashlib.md5(
            input_hts_fpath.encode('utf-8')
        ).hexdigest()
    # end def

    def count_classification_records(self, input_hts_fpath : str) -> int:
        classif_fpath = self.make_classification_fpath(
            input_hts_fpath
        )
        if not os.path.isfile(classif_fpath):
            return 0
        # end if
        with open(classif_fpath, 'rt') as input_handle:
            n_lines = len(input_handle.readlines())
        # end with
        count = n_lines - 2 # minus comment and minus header
        if count > 0:
            return count
        else:
            return 0
        # end if
    # end def

    def remove_workdir_files(self):
        classification_dirpath = self.make_classification_dir_path()
        tmp_dirpath = self.make_tmp_dir_path()
        for dirpath in (classification_dirpath, tmp_dirpath):
            if os.path.isdir(dirpath):
                logging.info('Emptying directory: `{}`...'.format(dirpath))
                fs.empty_dir(dirpath)
            # end if
        # end for

        files_to_rm = (
            os.path.join(self.work_dirpath, SEQDB_DB_FILE_NAME),
            os.path.join(self.work_dirpath, TAX_DB_FILE_NAME),
        )
        for fpath in files_to_rm:
            if os.path.isfile(fpath):
                logging.info('Removing file: `{}`...'.format(fpath))
                os.unlink(fpath)
            # end if
        # end for
        logging.info('Old results have been deleted.')
    # end def

    def archive_workdir_files(self):
        archive_dirpath = self.make_archive_dirpath()
        os.mkdir(archive_dirpath)
        self._archive_classification_dir(archive_dirpath)
        self._archive_seq_db_list_file(archive_dirpath)
        self._archive_taxonomy_file(archive_dirpath)
        self._empty_blast_tmp_dir()
        return archive_dirpath
    # end def

    def make_archive_dirpath(self):
        time_str = humane_time() \
            .replace(' ', '') \
            .replace(':', '') \
            .replace('-', '')
        archive_dirpath = os.path.join(
            self.work_dirpath,
            'archive_{}'.format(time_str)
        )

        if os.path.isdir(archive_dirpath):
            big_number, complex_archive_dirpath = 10, None
            for i in range(big_number):
                complex_archive_dirpath = '{}_{}'.format(
                    archive_dirpath,
                    big_number
                )
                if not os.path.isdir(complex_archive_dirpath):
                    archive_dirpath = complex_archive_dirpath
                    break
                # end if
            # end for
            if complex_archive_dirpath != archive_dirpath:
                logging.critical('Error: cannot archive classification directory')
                logging.critical(
                    'Maximum number of archive directories per second exceeded: {}' \
                        .format(big_number)
                )
                sys.exit(1)
            # end if
        # end if
        return archive_dirpath
    # end def

    def _archive_classification_dir(self, archive_dirpath : str):
        classification_dirpath = self.make_classification_dir_path()
        classif_archive_dirpath = os.path.join(archive_dirpath, 'classification')
        os.mkdir(classif_archive_dirpath)

        logging.info(
            'Archiving classification directory: `{}` -> `{}`...' \
                .format(classification_dirpath, classif_archive_dirpath)
        )

        classif_fpaths = glob.glob(
            os.path.join(
                classification_dirpath,
                '*'
            )
        )

        for fpath in classif_fpaths:
            if os.path.isfile(fpath):
                dest_fpath = os.path.join(
                    classif_archive_dirpath,
                    os.path.basename(fpath) + '.gz'
                )
                logging.info(
                    'Gzipping file `{}` -> `{}`'.format(
                        fpath, dest_fpath
                    )
                )
                fs.gzip_file(fpath, dest_fpath)
                os.unlink(fpath)
            elif os.path.isdir(fpath):
                dest_fpath = os.path.join(
                    classif_archive_dirpath,
                    os.path.basename(fpath)
                )
                logging.info(
                    'Moving directory `{}` -> `{}`'.format(
                        fpath, dest_fpath
                    )
                )
                os.rename(fpath, dest_fpath)
            # end if
        # end for
        logging.info('Archivation is completed.')

        return classif_archive_dirpath
    # end def

    def _archive_seq_db_list_file(self, archive_dirpath : str):
        seq_db_list_fpath = os.path.join(self.work_dirpath, SEQDB_DB_FILE_NAME)
        if os.path.isfile(seq_db_list_fpath):
            dest_fpath = os.path.join(
                archive_dirpath,
                '{}.gz'.format(SEQDB_DB_FILE_NAME)
            )
            logging.info(
                'Gzipping file `{}` -> `{}`'.format(
                    seq_db_list_fpath, dest_fpath
                )
            )
            fs.gzip_file(seq_db_list_fpath, dest_fpath)
            os.unlink(seq_db_list_fpath)
        # end if
    # end def

    def _archive_taxonomy_file(self, archive_dirpath : str):
        taxonomy_fpath = os.path.join(self.work_dirpath, TAX_DB_FILE_NAME)
        if os.path.isfile(taxonomy_fpath):
            dest_fpath = os.path.join(
                archive_dirpath,
                '{}.gz'.format(TAX_DB_FILE_NAME)
            )
            logging.info(
                'Gzipping file `{}` -> `{}`'.format(
                    taxonomy_fpath, dest_fpath
                )
            )
            fs.gzip_file(taxonomy_fpath, dest_fpath)
            os.unlink(taxonomy_fpath)
        # end if
    # end def

    def _empty_blast_tmp_dir(self):
        tmp_dirpath = self.make_tmp_dir_path()
        logging.info('Emptying temporary directory: `{}`...'.format(tmp_dirpath))
        fs.empty_dir(tmp_dirpath)
        logging.info('Done.')
    # end def


    def make_tmp_remote_blast_fpath(self, input_hts_fpath : str) -> str:
        classif_hash = self.make_classif_hash(input_hts_fpath)
        return os.path.join(
            self.make_tmp_dir_path(),
            '{}_tmp.json'.format(classif_hash)
        )
    # end def

    def write_tmp_remote_blast_file(self,
                                    request_id : str,
                                    input_hts_fpath : str,
                                    packet : SeqPacket):
        tmp_fpath = self.make_tmp_remote_blast_fpath(input_hts_fpath)
        quality_dict = make_quality_dict(packet)
        tmp_data = {
            'fpath' : input_hts_fpath,
            'request_id' : request_id,
            'packet_size' : len(packet),
            'quality_dict' : quality_dict,
        }
        with open(tmp_fpath, 'wt') as output_handle:
            json.dump(
                tmp_data,
                output_handle
            )
        # end with
    # end def

    def load_tmp_remote_blast_file(self,
                                   input_hts_fpath : str) -> dict:
        tmp_fpath = self.make_tmp_remote_blast_fpath(input_hts_fpath)
        if not os.path.exists(tmp_fpath):
            return None
        # end if
        with open(tmp_fpath, 'rt') as input_handle:
            tmp_data = json.load(input_handle)
        # end with

        # Don't load if full input file paths do not match
        if tmp_data['fpath'] != input_hts_fpath:
            return None
        # end if
        return tmp_data
    # end def

    def rm_tmp_remote_blast_file(self,
                                 input_hts_fpath : str):
        tmp_fpath = self.make_tmp_remote_blast_fpath(input_hts_fpath)
        if os.path.exists(tmp_fpath):
            os.unlink(tmp_fpath)
        # end if
    # end def


    def write_classification_header(self, input_hts_fpath : str):
        classif_fpath = self.make_classification_fpath(input_hts_fpath)
        with open(classif_fpath, 'wt') as output_handle:
            output_handle.write(
                '{} This is the classification for the file {}\n' \
                    .format(COMMENT_CHAR, input_hts_fpath)
            )
            output_handle.write(
                AlignResult.get_header_str()
            )
        # end with
    # end def
# end class
