import pytest
import datetime
from ledgertools import mint
from ledgertools.transaction import Transaction


test_mint_data = 'tests/data/mint_transactions_example.csv'


def test_get_data():
    actual = mint.get_data('tests/data/mint_transactions_basic.csv')
    expected = [
        Transaction(
            account_name = 'CREDIT CARD',
            amount = '1250.00',
            category = 'Gift',
            date = datetime.date(2016, 10, 10),
            description = 'Example Description',
            labels = '',
            notes = '',
            original_description = 'FULL DESCRIPTION',
            transaction_type = 'debit'
        ),
        Transaction(
            account_name = 'CHECKING',
            amount = '5.00',
            category = 'Bank Fee',
            date = datetime.date(2011, 4, 7),
            description = 'Xxxxxxx Xxxxxxxxxxx Xxx',
            labels = '',
            notes = '',
            original_description = 'XXXXXXX XXXXXXX XXX',
            transaction_type = 'debit'
        ),
        Transaction(
            account_name = 'CREDIT CARD',
            amount = '50.57',
            category = 'Gas & Fuel',
            date = datetime.date(2011, 4, 8),
            description = 'Xxxxxx',
            labels = '',
            notes = '',
            original_description = 'XXXXXX 1231231231',
            transaction_type = 'debit'
        ),
    ]

    assert actual == expected


def test_pending_filter():
    mint_trans = mint.get_data(test_mint_data)
    filtered = mint.filter_pending_trans(mint_trans)

    assert mint_trans[3:] == filtered


def test_pending_filter_no_pending():
    mint_trans = mint.get_data('tests/data/mint_transactions_no_pending.csv')
    filtered = mint.filter_pending_trans(mint_trans)

    assert mint_trans == filtered


def test_pending_filter_broken():
    mint_trans = mint.get_data('tests/data/mint_transactions_broken.csv')
    with pytest.raises(Exception):
        mint.filter_pending_trans(mint_trans)
