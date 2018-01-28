from contextlib import contextmanager
import pytest
from click.testing import CliRunner
import os


@pytest.fixture
def runner():
    return CliRunner()

def read_file(path):
    with open(path, 'r') as infile:
        return infile.read()

def write_file(name, content):
    os.makedirs(os.path.dirname(name), exist_ok=True)
    with open(name, 'w') as outfile:
        outfile.write(content)

@contextmanager
def get_iso_filesystem(files_to_copy, runner):
    # Load files to be used in the isolated filesystem
    file_content_pairs = []
    for path in files_to_copy:
        file_content_pairs.append((path, read_file(path)))

    with runner.isolated_filesystem() as iso:
        for name, content in file_content_pairs:
            write_file(name, content)

        yield iso
