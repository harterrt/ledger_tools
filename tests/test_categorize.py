import pytest
import os.path
import pickle
import click
from click import _termui_impl
from click.testing import CliRunner
from collections import namedtuple

from ledgertools import cli
from ledgertools import ledger
from ledgertools.categorize import to_ledger_format
from .data import new_transactions
from .utils import runner, get_iso_filesystem


KB_INTERRUPT = '\x03'
ESCAPE = '\x1b'


@pytest.fixture
def nt():
    return new_transactions


@pytest.fixture
def runner():
    return CliRunner()


def ledger_load(path):
    if os.path.isfile(path):
        return ledger.get_transactions(path)
    else:
        return None


def pickle_load(path):
    try:
        with open(path, 'rb') as infile:
            return pickle.load(infile)
    except FileNotFoundError:
        return None


def pickle_dump(path, obj):
    with open(path, 'wb') as outfile:
        pickle.dump(obj, outfile)


def run_categorize(new_transactions, ledger_path, user_input, runner,
                   monkeypatch):
    # Generic noop for mocking out curses
    def noop(*a):
        pass

    # Make sure `pick` uses the input from the click runner
    def mock_getch():
        char = click.termui._getchar(False)
        _termui_impl._translate_ch_to_exc(char)
        return ord(char)

    # Mock out curses so we don't screw with the screen during testing
    def mock_curses_wrapper(func):
        fake_screen = namedtuple('fake_screen',
                                 ['clear', 'getmaxyx', 'addnstr', 'refresh',
                                  'getch'])
        return func(fake_screen(noop, lambda: (100, 100), noop, noop,
                                mock_getch))

    monkeypatch.setattr(cli.cat.pick.curses, 'wrapper', mock_curses_wrapper)
    monkeypatch.setattr(cli.cat.pick.curses, 'use_default_colors', noop)
    monkeypatch.setattr(cli.cat.pick.curses, 'curs_set', noop)
    monkeypatch.setattr(cli.cat.pick.curses, 'init_pair', noop)

    with get_iso_filesystem([ledger_path], runner):
        new_trans_path = 'new_trans.pickle'
        new_ledger_path = 'new_trans.ledger'

        # Save new trans and ledger file to temp filesystem
        pickle_dump(new_trans_path, new_transactions)

        # Run the categorization
        runner.invoke(cli.categorize, [
            '--new',
            new_trans_path,
            '--ledger',
            ledger_path,
            '--out',
            new_ledger_path,
        ], input=user_input, catch_exceptions=False)

        CatFiles = namedtuple(
            'cat_files',
            ['new_trans', 'ledger_trans'],
        )

        out = CatFiles(pickle_load(new_trans_path),
                       ledger_load(new_ledger_path))

    return out


def formatter(trans, category):
    return to_ledger_format(trans, category)


def test_cat_abort(runner, monkeypatch, nt):
    cat_files = run_categorize(nt.many_new_transactions,
                               'tests/data/categorize.ledger',
                               KB_INTERRUPT, runner, monkeypatch)

    assert cat_files.ledger_trans is None
    assert cat_files.new_trans == nt.many_new_transactions


def test_single_cat(runner, monkeypatch, nt):
    cat_files = run_categorize(nt.many_new_transactions,
                               'tests/data/categorize.ledger',
                               'j\n' + KB_INTERRUPT, runner, monkeypatch)

    assert cat_files.ledger_trans[0]['category'] == 'Expenses:Food:Eating Out'
    assert cat_files.new_trans == nt.many_new_transactions[:-1]


def test_multiple_cat(runner, monkeypatch, nt):
    cat_files = run_categorize(nt.many_new_transactions,
                               'tests/data/categorize.ledger',
                               'j\n\n' + KB_INTERRUPT, runner, monkeypatch)

    assert len(cat_files.ledger_trans) == 4  # Every tran has 2 lines
    assert cat_files.ledger_trans[0]['category'] == 'Expenses:Food:Eating Out'
    assert cat_files.ledger_trans[1]['category'] == 'CREDIT CARD'


def test_case_insensitive_search(runner, monkeypatch, nt):
    cat_files = run_categorize(nt.many_new_transactions,
                               'tests/data/categorize.ledger',
                               ('/eat' + ESCAPE +
                                '/card' + ESCAPE + '\n' + KB_INTERRUPT),
                               runner, monkeypatch)

    assert cat_files.ledger_trans[0]['category'] == 'CREDIT CARD'


def test_search(runner, monkeypatch, nt):
    cat_files = run_categorize(nt.many_new_transactions,
                               'tests/data/categorize.ledger',
                               '/eat' + ESCAPE + '\n' + KB_INTERRUPT,
                               runner, monkeypatch)

    assert cat_files.ledger_trans[0]['category'] == 'Expenses:Food:Eating Out'


def test_naive_bayes(runner, monkeypatch, nt):
    cat_files = run_categorize(nt.many_new_transactions,
                               'tests/data/categorize.ledger',
                               'b' + '\n' + KB_INTERRUPT,
                               runner, monkeypatch)

    assert cat_files.ledger_trans[0]['category'] == 'Expenses:Utilities:Gas'
