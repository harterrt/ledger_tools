from click.testing import CliRunner
import pytest
import pickle
from ledgertools import cli
from .test_mint import test_mint_data
from .utils import runner, get_iso_filesystem
# Make this a fixture instead
from .data import new_transactions as nt



def test_cli(runner):
    result = runner.invoke(cli.pull_mint)
    assert result.exit_code == 0
    assert not result.exception
    assert "mint.com" in result.output


def test_account_override(runner):
    files = {
        'mint': test_mint_data,
        'ledger': 'tests/data/example.ledger',
        'settings': 'tests/data/overrides.py',
    }
    with get_iso_filesystem([path for key, path in files.items()], runner):
        outfile = 'tmp.pickle'
        results = runner.invoke(cli.dump_new_trans, [
            '--out', outfile,
            '--mint', files['mint'],
            '--ledger', files['ledger'],
            '--settings', files['settings'],
        ])
        print(results.output)
        with open(outfile, 'rb') as f:
            actual = pickle.load(f)

    expected = nt.new_transactions.copy()
    expected[0]['account'] = 'Liabilities:CreditCard'
    assert expected == actual
