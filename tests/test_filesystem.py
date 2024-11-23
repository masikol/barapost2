
import os
from typing import Sequence

import pytest

import src.filesystem as fs


RAW_NANOPORE_EXTENSIONS = (
    'fast5',
    'pod5',
    'blow5',
    'slow5',
)


# === Fixtures ===

@pytest.fixture
def fasta_file_paths_plain() -> Sequence[str]:
    return tuple(
        map(
            lambda x: os.path.join('path', 'name.{}'.format(x)),
            fs.FASTA_EXTENSIONS
        )
    )
# end def

@pytest.fixture
def fasta_file_paths_gzipped() -> Sequence[str]:
    return tuple(
        map(
            lambda x: os.path.join('path', 'name.{}.gz'.format(x)),
            fs.FASTA_EXTENSIONS
        )
    )
# end def

@pytest.fixture
def non_fasta_file_paths() -> Sequence[str]:
    return tuple(
        map(
            lambda x: os.path.join('path', 'name.{}ERROR'.format(x)),
            fs.FASTA_EXTENSIONS
        )
    )
# end def


@pytest.fixture
def fastq_file_paths_plain() -> Sequence[str]:
    return tuple(
        map(
            lambda x: os.path.join('path', 'name.{}'.format(x)),
            fs.FASTQ_EXTENSIONS
        )
    )
# end def

@pytest.fixture
def fastq_file_paths_gzipped() -> Sequence[str]:
    return tuple(
        map(
            lambda x: os.path.join('path', 'name.{}.gz'.format(x)),
            fs.FASTQ_EXTENSIONS
        )
    )
# end def

@pytest.fixture
def non_fastq_file_paths() -> Sequence[str]:
    return tuple(
        map(
            lambda x: os.path.join('path', 'name.{}ERROR'.format(x)),
            fs.FASTQ_EXTENSIONS
        )
    )
# end def


@pytest.fixture
def raw_nanopore_file_paths() -> Sequence[str]:
    return tuple(
        map(
            lambda x: os.path.join('path', 'name.{}'.format(x)),
            RAW_NANOPORE_EXTENSIONS
        )
    )
# end def

@pytest.fixture
def non_raw_nanopore_file_paths() -> Sequence[str]:
    return tuple(
        map(
            lambda x: os.path.join('path', 'name.{}ERROR'.format(x)),
            RAW_NANOPORE_EXTENSIONS
        )
    )
# end def


@pytest.fixture
def a_path_with_bad_chars() -> str:
    file_path = os.path.join('some', 'arbitrary', 'path.txt')
    for char in fs._BAD_CHARS:
        file_path += char
    # end for
    return file_path
# end def


# === Test classes ===

class TestIsFasta:

    def test_plain_fasta_paths(self, fasta_file_paths_plain):
        assert all(
            map(
                fs.is_fasta,
                fasta_file_paths_plain
            )
        )
    # end def

    def test_gzipped_fasta_paths(self, fasta_file_paths_gzipped):
        assert all(
            map(
                fs.is_fasta,
                fasta_file_paths_gzipped
            )
        )
    # end def

    def test_non_fasta_paths(self, non_fasta_file_paths):
        assert not any(
            map(
                fs.is_fasta,
                non_fasta_file_paths
            )
        )
    # end def
# end class


class TestIsFastq:

    def test_plain_fastq_paths(self, fastq_file_paths_plain):
        assert all(
            map(
                fs.is_fastq,
                fastq_file_paths_plain
            )
        )
    # end def

    def test_gzipped_fastq_paths(self, fastq_file_paths_gzipped):
        assert all(
            map(
                fs.is_fastq,
                fastq_file_paths_gzipped
            )
        )
    # end def

    def test_non_fastq_paths(self, non_fastq_file_paths):
        assert not any(
            map(
                fs.is_fastq,
                non_fastq_file_paths
            )
        )
    # end def
# end class


class TestIsRawNanopore:

    def test_raw_nanopore_paths(self, raw_nanopore_file_paths):
        assert fs.is_fast5(raw_nanopore_file_paths[0])
        assert fs.is_pod5( raw_nanopore_file_paths[1])
        assert fs.is_blow5(raw_nanopore_file_paths[2])
        assert fs.is_slow5(raw_nanopore_file_paths[3])
    # end def

    def test_non_raw_nanopore_paths(self, non_raw_nanopore_file_paths):
        assert not fs.is_fast5(non_raw_nanopore_file_paths[0])
        assert not fs.is_pod5( non_raw_nanopore_file_paths[1])
        assert not fs.is_blow5(non_raw_nanopore_file_paths[2])
        assert not fs.is_slow5(non_raw_nanopore_file_paths[3])
    # end def
# end class


class TestRemoveBadChars:

    def test_remove_bad_chars(self, a_path_with_bad_chars):
        processed_str = fs.remove_bad_chars(a_path_with_bad_chars)
        for char in fs._BAD_CHARS:
            assert not char in processed_str
        # end for
    # end def
# end class
