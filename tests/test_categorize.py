import pytest
import click
from click import _termui_impl
from click.testing import CliRunner
from ledgertools import cli
from .data import new_transactions as nt
import pickle
from collections import namedtuple


KB_INTERRUPT = '\x03'


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


def run_categorize(new_transactions, ledger_path, user_input, runner, monkeypatch):
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
        return func(fake_screen(noop, lambda : (100, 100), noop, noop, mock_getch))

    monkeypatch.setattr(cli.cat.pick.curses, 'wrapper', mock_curses_wrapper)
    monkeypatch.setattr(cli.cat.pick.curses, 'use_default_colors', lambda: None)
    monkeypatch.setattr(cli.cat.pick.curses, 'curs_set', lambda a: None)
    monkeypatch.setattr(cli.cat.pick.curses, 'init_pair', lambda a, b, c: None)

    # Load the ledger data to be used in the isolated filesystem
    with open(ledger_path) as infile:
        ledger_text = infile.read()


    with runner.isolated_filesystem():
        new_trans_path = 'new_trans.pickle'
        existing_ledger_path = 'existing.ledger'
        new_ledger_path = 'new_trans.ledger'

        # Save new trans and ledger file to temp filesystem
        pickle_dump(new_trans_path, new_transactions)
        with open(existing_ledger_path, 'w') as tmpfile:
            tmpfile.write(ledger_text)

        result = runner.invoke(cli.categorize, [
            '--new-trans',
            new_trans_path,
            '--ledger-path',
            existing_ledger_path,
            '--out-path',
            new_ledger_path,
        ], input=user_input, catch_exceptions=False)



        CatFiles = namedtuple(
            'cat_files',
            ['new_trans', 'ledger_trans'],
        )

        out = CatFiles(load(new_trans_path), load(new_ledger_path))

    return out


def test_cat_abort(runner, monkeypatch):
    cat_files = run_categorize(nt.many_new_transactions,
                               'tests/data/categorize.ledger',
                               KB_INTERRUPT, runner, monkeypatch)

    assert cat_files.ledger_trans is None
    assert cat_files.new_trans == nt.many_new_transactions


# This currently fails, because categorize does nothing
def test_single_cat(runner, monkeypatch):
    cat_files = run_categorize(nt.many_new_transactions,
                               'tests/data/categorize.ledger',
                               '\n' + KB_INTERRUPT, runner, monkeypatch)

    assert cat_files.ledger_trans is not None
    assert cat_files.ledger_trans != ''
    assert cat_files.new_trans == nt.many_new_transactions[:-1]
