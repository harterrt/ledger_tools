from ledgertools import ledger
from .data.parsed_ledger_data import parsed_ledger_data


def test_get_transactions():
    actual = ledger.get_transactions('tests/data/example.ledger')
    expected = parsed_ledger_data

    assert actual == expected
