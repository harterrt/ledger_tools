from contextlib import contextmanager
from copy import deepcopy
from ledgertools import config
import pytest
from click.testing import CliRunner
import os


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture()
def nt():
    from .data import new_transactions
    print(new_transactions.new_transactions)
    return new_transactions


def read_file(path):
    with open(path, 'r') as infile:
        return infile.read()


def write_file(name, content):
    os.makedirs(os.path.dirname(name), exist_ok=True)
    with open(name, 'w') as outfile:
        outfile.write(content)


@contextmanager
def isolated_settings():
    base_settings = deepcopy(config.settings)
    yield
    config.settings = base_settings


@contextmanager
def get_iso_filesystem(files_to_copy, runner):
    # Load files to be used in the isolated filesystem
    file_content_pairs = []
    for path in files_to_copy:
        file_content_pairs.append((path, read_file(path)))

    with isolated_settings():
        with runner.isolated_filesystem() as iso:
            for name, content in file_content_pairs:
                write_file(name, content)

            yield iso
