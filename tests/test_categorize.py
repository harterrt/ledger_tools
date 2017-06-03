import pytest
from click.testing import CliRunner
from ledgertools import cli
from .data import new_transactions as nt
import pickle
from collections import namedtuple


@pytest.fixture
def runner():
    return CliRunner()


def load(path):
    try:
        if 'pickle' in path:
            with open(path, 'rb') as infile:
                return pickle.load(infile)
        else:
            with open(path, 'r') as infile:
                return infile.read()

    except FileNotFoundError:
        return None


def pickle_dump(path, obj):
    with open(path, 'wb') as outfile:
        pickle.dump(obj, outfile)


def run_categorize(ledger_path, new_transactions, user_input, runner):
    with open(ledger_path) as infile:
        ledger_text = infile.read()

    with runner.isolated_filesystem():
        new_trans_path = 'new_trans.pickle'
        new_ledger_path = 'new_trans.ledger'

        # Save new trans to temp filesystem
        pickle_dump(new_trans_path, new_transactions)

        with open('categorize.ledger', 'w') as tmpfile:
            tmpfile.write(ledger_text)

        runner.invoke(cli.categorize, [
            '--new-trans',
            new_trans_path,
            '--out-file',
            new_ledger_path,
        ], input=user_input)

        CatFiles = namedtuple(
            'cat_files',
            ['new_trans', 'ledger_trans'],
        )

        return CatFiles(load(new_trans_path), load(new_ledger_path))


def test_cat_abort(runner):
    cat_files = run_categorize('tests/data/categorize.ledger',
                               nt.many_new_transactions, '^C', runner)

    assert cat_files.ledger_trans is None
    assert cat_files.new_trans == nt.many_new_transactions


# This currently fails, because categorize does nothing
# def test_single_cat(runner):
#     cat_files = run_categorize('tests/data/categorize.ledger',
#                                nt.many_new_transactions, '\n^C', runner)
#
#     assert cat_files.ledger_trans != None
#     assert cat_files.new_trans == nt.many_new_transactions[1:]
