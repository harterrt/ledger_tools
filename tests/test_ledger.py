from ledgertools import ledger
from .utils import load_data


def test_get_transactions():
    actual = ledger.get_transactions('tests/data/example.ledger')
    expected = load_data('tests/data/parsed_ledger_data.pickle')

    assert actual == expected
