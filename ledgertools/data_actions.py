from collections import namedtuple
from .utils import dump_amount
from . import mint, ledger


TransactionKey = namedtuple(
    'TransactionKey',
    ['date', 'amount', 'description']
)


def key_mint_tran(mint_tran):
    return (
        TransactionKey(
            mint_tran['date'],
            mint_tran['amount'],
            mint_tran['description']
        ),
        mint_tran
    )


def simplify_ledger_tran(ledger_tran):
    return TransactionKey(
        ledger_tran['date'],
        ledger_tran['amount'],
        ledger_tran['payee']
    )


def is_recorded(keyed_mint_tran, simple_ledger_trans):
    return keyed_mint_tran[0] in simple_ledger_trans


def trans_filter(ledger_trans):
    """Return a filter function for a given set of ledger transactions

    This implementation is naive, but this format makes it easy to refactor
    to a statistical filter if we have performance issues"""
    simple_ledger_trans = list(map(simplify_ledger_tran, ledger_trans))
    return lambda mint_tran: not is_recorded(mint_tran, simple_ledger_trans)


def find_new(mint_trans, ledger_trans):
    """Finds mint trans not yet included in a list of ledger trans"""
    keyed_trans = list(map(key_mint_tran, mint_trans))
    new_trans = list(filter(trans_filter(ledger_trans), keyed_trans))

    print(list(keyed_trans))
    print('-'*80)
    print(list(map(simplify_ledger_tran, ledger_trans)))
    print('-'*80)
    print(new_trans)
    return list(map(lambda x: x[1], new_trans))


def new_trans_from_path(mint_path, ledger_path):
    return find_new(mint.get_transactions(mint_path),
                    ledger.get_transactions(ledger_path))
