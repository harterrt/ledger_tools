from ledgertools import data_actions, mint, ledger

test_mint_data = 'tests/data/mint_transactions_example.csv'


def test_find_new(nt):
    mint_trans = mint.get_transactions(test_mint_data)
    ledger_trans = ledger.get_transactions('tests/data/example.ledger')

    new = data_actions.find_new(mint_trans, ledger_trans)

    assert new == nt.new_transactions


def test_new_trans_from_path(nt):
    new = data_actions.new_trans_from_path(test_mint_data,
                                           'tests/data/example.ledger')

    assert new == nt.new_transactions


def test_new_trans_with_split_tran(nt):
    new = data_actions.new_trans_from_path(test_mint_data,
                                           'tests/data/split_tran.ledger')

    assert new == nt.new_transactions


def test_new_trans_with_small_amount(nt):
    small_mint_trans = 'tests/data/mint_transactions_small_tran.csv'
    new = data_actions.new_trans_from_path(small_mint_trans,
                                           'tests/data/small_tran.ledger')

    assert new == nt.new_transactions
