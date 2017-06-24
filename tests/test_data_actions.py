from ledgertools import data_actions, mint, ledger
from .test_mint import test_mint_data
from .data.new_transactions import new_transactions


def test_find_new():
    mint_trans = mint.get_transactions(test_mint_data)
    ledger_trans = ledger.get_transactions('tests/data/example.ledger')

    new = data_actions.find_new(mint_trans, ledger_trans)

    assert new == new_transactions


def test_new_trans_from_path():
    new = data_actions.new_trans_from_path(test_mint_data,
                                           'tests/data/example.ledger')

    assert new == new_transactions


def test_new_trans_with_split_tran():
    new = data_actions.new_trans_from_path(test_mint_data,
                                           'tests/data/split_tran.ledger')

    assert new == new_transactions
