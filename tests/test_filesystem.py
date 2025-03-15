
import os
import gzip
from typing import Sequence

from pathlib import Path

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


@pytest.fixture
def real_plain_fpath() -> str:
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'test_read_write',
        'data',
        'test_input',
        'some_seqs.fasta'
    )
# end def


@pytest.fixture
def real_gziped_fpath() -> str:
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'test_read_write',
        'data',
        'test_input',
        'some_seqs.fasta.gz'
    )
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
        # assert fs.is_blow5(raw_nanopore_file_paths[2]) # TODO: add S/BLOW5 support
        # assert fs.is_slow5(raw_nanopore_file_paths[3]) # TODO: add S/BLOW5 support
    # end def

    def test_non_raw_nanopore_paths(self, non_raw_nanopore_file_paths):
        assert not fs.is_fast5(non_raw_nanopore_file_paths[0])
        assert not fs.is_pod5( non_raw_nanopore_file_paths[1])
        # assert not fs.is_blow5(non_raw_nanopore_file_paths[2]) # TODO: add S/BLOW5 support
        # assert not fs.is_slow5(non_raw_nanopore_file_paths[3]) # TODO: add S/BLOW5 support
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


class TestGzip:

    def test_is_gzipped_plain_file(self,
                                   fasta_file_paths_plain : Sequence[str]):
        file_path = next(iter(fasta_file_paths_plain))
        assert fs.is_gzipped(file_path) == False
    # end def

    def test_is_gzipped_gzipped_file(self,
                                     fasta_file_paths_gzipped : Sequence[str]):
        file_path = next(iter(fasta_file_paths_gzipped))
        assert fs.is_gzipped(file_path) == True
    # end def

    def test_stop_if_bad_gzip_file_gzipped(self,
                                           real_gziped_fpath : str):
        try:
            fs.stop_if_bad_gzip_file(real_gziped_fpath)
        except SystemExit:
            assert False, 'test_test_gzip_file_ok_gzipped caught SystemExit'
        # end try
    # end def

    def test_stop_if_bad_gzip_file_plain(self,
                                         real_plain_fpath : str):
        with pytest.raises(SystemExit):
            fs.stop_if_bad_gzip_file(real_plain_fpath)
        # end with
    # end def
# end class

# remove_file_extension test
def test_remove_file_extension_normal() -> None:
    file_path = os.path.join('folder', 'file.fasta')
    expected = os.path.join('folder', 'file')
    assert fs.remove_file_extension(file_path) == expected
# end def

def test_remove_file_extension_multiple_dots() -> None:
    file_path = os.path.join('folder', 'archive.tar.gz')
    expected = os.path.join('folder', 'archive.tar')
    assert fs.remove_file_extension(file_path) == expected
# end def

def test_remove_file_extension_no_extension() -> None:
    file_path = os.path.join('folder', 'file')
    assert fs.remove_file_extension(file_path) == file_path
# end def

def test_remove_file_extension_trailing_dot() -> None:
    file_path = os.path.join('folder', 'file.')
    expected = os.path.join('folder', 'file')
    assert fs.remove_file_extension(file_path) == expected
# end def

def test_remove_file_extension_hidden_file() -> None:
    file_path = os.path.join('folder', '.bashrc')
    expected = os.path.join('folder', '')
    assert fs.remove_file_extension(file_path) == expected
# end def

# gzip_file test
def test_gzip_file_normal(tmp_path: Path) -> None:
    fasta_content: bytes = b'>seq1\nATCGATCGATCG\n'
    src_file: Path = tmp_path / 'sample.fasta'
    src_file.write_bytes(fasta_content)

    dest_file: Path = tmp_path / 'sample.fasta.gz'
    fs.gzip_file(str(src_file), str(dest_file))

    assert dest_file.exists()
    with gzip.open(str(dest_file), 'rb') as f:
        decompressed: bytes = f.read()
    # end with
    assert decompressed == fasta_content
# end def

def test_gzip_file_empty(tmp_path: Path) -> None:
    src_file: Path = tmp_path / 'empty.fasta'
    src_file.write_bytes(b'')

    dest_file: Path = tmp_path / 'empty.fasta.gz'
    fs.gzip_file(str(src_file), str(dest_file))

    with gzip.open(str(dest_file), 'rb') as f:
        decompressed: bytes = f.read()
    # end with
    assert decompressed == b''
# end def

def test_gzip_file_overwrite(tmp_path: Path) -> None:
    fasta_content: bytes = b'>seq2\nGTCAGTCAGTCA\n'
    src_file: Path = tmp_path / 'data.fasta'
    src_file.write_bytes(fasta_content)

    dest_file: Path = tmp_path / 'data.fasta.gz'
    dest_file.write_text('>old_seq\nNNNNNNNNNN\n')

    fs.gzip_file(str(src_file), str(dest_file))
    with gzip.open(str(dest_file), 'rb') as f:
        decompressed: bytes = f.read()
    # end with
    assert decompressed == fasta_content
# end def

# empty_dir
def test_empty_dir_already_empty(tmp_path: Path) -> None:
    empty_directory: Path = tmp_path / 'empty_dir'
    empty_directory.mkdir()
    fs.empty_dir(str(empty_directory))
    assert list(empty_directory.iterdir()) == []
# end def

def test_empty_dir_with_files(tmp_path: Path) -> None:
    test_dir: Path = tmp_path / 'dir_files'
    test_dir.mkdir()
    (test_dir / 'a.fasta').write_text('>seqA\nATCG')
    (test_dir / 'b.fastq').write_text('@seqB\nGTCAGT\n+\n!!!!!!')

    fs.empty_dir(str(test_dir))
    assert list(test_dir.iterdir()) == []
# end def

def test_empty_dir_with_subdirectories(tmp_path: Path) -> None:
    test_dir: Path = tmp_path / 'dir_nested'
    test_dir.mkdir()
    sub_dir: Path = test_dir / 'subdir'
    sub_dir.mkdir()
    (sub_dir / 'file.fasta').write_text('>seq_nested\nATCGATCG')

    fs.empty_dir(str(test_dir))
    assert list(test_dir.iterdir()) == []
# end def

def test_empty_dir_nonexistent(tmp_path: Path) -> None:
    non_exist_dir: Path = tmp_path / 'nonexistent'
    try:
        fs.empty_dir(str(non_exist_dir))
    except Exception as e:
        pytest.fail(f'empty_dir raise exception on unexisting directory: {e}')
    # end try
# end def
