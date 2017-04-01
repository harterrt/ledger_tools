from ledger_tools import data_actions, mint, ledger
from .test_mint import *

def test_find_new():
    mint_trans = mint.get_transactions(test_mint_data)
    ledger_trans = ledger.get_transactions('tests/data/example.ledger')

    new = data_actions.find_new(mint_trans, ledger_trans)
    print(new)

    assert new == []

