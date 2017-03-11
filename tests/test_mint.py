import pytest
import pickle
from ledger_tools import mint

test_mint_data = 'tests/data/example_mint_transactions.csv'
raw_mint_data = 'tests/data/raw_mint_data.pickle'

def test_get_data():
    actual = mint.get_raw_data(test_mint_data)
    with open(raw_mint_data, 'r') as infile:
        expected = pickle.load(infile)

    assert actual == expected



