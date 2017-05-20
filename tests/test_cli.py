import pytest
from click.testing import CliRunner
from ledgertools import cli
from .data import new_transactions as nt
import pickle


@pytest.fixture
def runner():
    return CliRunner()


def test_cli(runner):
    result = runner.invoke(cli.pull_mint)
    assert result.exit_code == 0
    assert not result.exception
    assert "mint.com" in result.output


def test_categorize(runner):
    with open('tests/data/categorize.ledger') as infile:
        ledger_text = infile.read()

    with runner.isolated_filesystem():
        # Save new trans to temp filesystem
        with open('new_trans.pickle', 'wb') as tmpfile:
            pickle.dump(nt.many_new_transactions, tmpfile)

        with open('categorize.ledger', 'w') as tmpfile:
            tmpfile.write(ledger_text)

        result = runner.invoke(cli.categorize, [
            '--new-trans',
            'new_trans.pickle',
            '--out-file',
            'new_trans.ledger',
        ], input='^C')

        with pytest.raises(FileNotFoundError):
            open('new_trans.ledger', 'r')
