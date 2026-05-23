# AGENTS.md - Barapost2 Development Guide

This document provides guidelines for AI agents working on the barapost2 codebase.

## Project Overview

Barapost2 is a bioinformatics tool for classifying nanopore sequencing reads via remote BLAST queries. It's a Python project with pytest testing, no CI/CD setup, and minimal configuration files.

## Build/Lint/Test Commands

### Running Tests

```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/test_filesystem.py

# Run single test (path format: module::Class::method)
python -m pytest tests/test_filesystem.py::TestIsFasta::test_plain_fasta_paths -v

# Run tests matching a pattern
python -m pytest -k "test_is_fasta"

# Run with verbose output
python -m pytest -v
```

### Linting/Type Checking

```bash
# Run mypy type checking
python -m mypy src/ tests/

# Run ruff linting (if configured)
python -m ruff check src/ tests/
```

### Dependencies

Dependencies are declared in `pyproject.toml`. Install via:
```bash
pip install -e .  # Editable install
```
Or:
```bash
pip install ont_fast5_api==4.1.3 pod5==0.3.23 pyslow5==1.3.0 pytest==8.3.4
```

## Code Style Guidelines

### Formatting

- Use 4 spaces for indentation (no tabs)
- Maximum line length: 100 characters (soft guideline)
- Use `.format()` for string formatting (legacy, but consistent with existing code)
- No automatic formatter configured

### Imports

- Use absolute imports: `import src.filesystem as fs`
- Group stdlib imports first, then third-party, then project imports
- One import per line

### Naming Conventions

- **Classes**: PascalCase (e.g., `ProberArgs`, `HTSRecord`)
- **Functions/variables**: snake_case (e.g., `is_fasta`, `get_file_extension`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `FASTA_EXTENSIONS`, `ACTION_RESUME`)
- **Private methods/attributes**: prefix with underscore (e.g., `_handle_previous_run`)

### Type Hints

- Use Python 3.12-compatible type hints
- Import from `typing` module: `Sequence`, `TypeAlias`, etc.
- Use `TypeAlias` for type aliases: `ActionCode : TypeAlias = str`
- Use explicit return type annotations on all functions

### Error Handling

- Use `logging` for non-fatal errors: `logging.critical()`, `logging.error()`, `logging.info()`
- Use `sys.exit(1)` for fatal errors that should terminate the program
- Use custom exception classes from appropriate modules (e.g., `TaxonomyParseError`, `RequestFailError`)
- Use `try/except` blocks with specific exception types

### Documentation

- No docstrings required (follows existing convention)
- Only add comments when critical for understanding
- Keep comments concise and factual
- Do NOT add comment headers for functions/classes

### Code Structure

- Follow existing module organization in `src/`
- Use `__init__.py` files in subdirectories
- Keep related functionality together (e.g., `src/containers/`, `src/reader_system/`)
- Abstract classes should raise `NotImplementedError()` in `__init__`

### Testing

- Use pytest fixtures with `@pytest.fixture` decorator
- Group tests in classes: `class TestIsFasta:`
- Test file naming: `test_*.py`
- Use type hints on fixture functions
- Test utilities in `tests/util.py`

### Git Conventions

- No enforced commit message format
- No pre-commit hooks configured
- Avoid committing large data files (see .gitignore)

## Project Directory Structure

```
barapost2/
├── src/
│   ├── args/           # Command-line argument parsing
│   ├── config/         # Configuration files
│   ├── containers/     # Data structures (HTSRecord, SeqRecord, etc.)
│   ├── network/       # Network request handling
│   ├── reader_system/ # File reading (FAST5, POD5, etc.)
│   ├── remote_blast/  # BLAST query handling
│   ├── seq_db/        # Sequence database management
│   ├── taxonomy/      # Taxonomy processing
│   ├── util/          # Utility functions
│   ├── writer_system/ # File writing
│   ├── filesystem.py  # File type detection utilities
│   ├── prober_kernel.py # Main application logic
│   └── time.py        # Time utilities
├── tests/              # Test suite
├── data/              # Test data
├── requirements.txt   # Python dependencies
├── pyproject.toml     # Project configuration
└── README.md          # Project documentation
```

## Common Patterns

### Checking file types
```python
import src.filesystem as fs
if fs.is_fasta(file_path): ...
if fs.is_fastq(file_path): ...
if fs.is_gzipped(file_path): ...
```

### Running the main application
```bash
python -m src.prober_kernel <arguments>
```

### Reading test files
```python
import tests.util as util
md5_sum = util.md5_file_sum(file_path)
```

## Notes for AI Agents

- This codebase uses old-style Python string formatting with `.format()` - maintain consistency
- There is no CI/CD pipeline; manual testing is required
- The project is under active development (as of 2025)
- Test data is located in `tests/*/data/` directories