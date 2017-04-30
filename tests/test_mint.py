import pytest
import datetime
from ledgertools import mint


test_mint_data = 'tests/data/mint_transactions_example.csv'


def test_parse_trans():
    actual = mint.parse_transaction({'date': '1/01/2017',
                                     'amount': '10.00',
                                     'other': 'stays the same'})
    expected = {'date': datetime.date(2017, 1, 1),
                'amount': '10.00',
                'other': 'stays the same'}

    assert actual == expected


def test_get_data():
    actual = mint.get_data('tests/data/mint_transactions_basic.csv')
    expected = [
        {
            'account name': 'CREDIT CARD',
            'amount': '1250.00',
            'category': 'Gift',
            'date': datetime.date(2016, 10, 10),
            'description': 'Example Description',
            'labels': '',
            'notes': '',
            'original description': 'FULL DESCRIPTION',
            'transaction type': 'debit'
        },
        {
            'account name': 'CHECKING',
            'amount': '5.00',
            'category': 'Bank Fee',
            'date': datetime.date(2011, 4, 7),
            'description': 'Xxxxxxx Xxxxxxxxxxx Xxx',
            'labels': '',
            'notes': '',
            'original description': 'XXXXXXX XXXXXXX XXX',
            'transaction type': 'debit'
        },
        {
            'account name': 'CREDIT CARD',
            'amount': '50.57',
            'category': 'Gas & Fuel',
            'date': datetime.date(2011, 4, 8),
            'description': 'Xxxxxx',
            'labels': '',
            'notes': '',
            'original description': 'XXXXXX 1231231231',
            'transaction type': 'debit'
        },
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
