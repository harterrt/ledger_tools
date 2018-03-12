import pytest
import datetime
from ledgertools import mint
from decimal import Decimal
from .test_categorize import run_categorize


test_mint_data = 'tests/data/mint_transactions_example.csv'

def test_parse_tran():
    actual = mint.parse_transaction({
        'Account Name': 'CREDIT CARD',
        'Amount': '2.50',
        'Category': 'Coffee Shop',
        'Date': '10/10/2016',
        'Description': 'Commonplace',
        'Labels': '',
        'Notes': '',
        'Original Description': 'COMMONPLACE COFFEE HOUSE',
        'Transaction Type': 'debit'
    })

    expected = {
        'account': 'CREDIT CARD',
        'amount': Decimal('-2.50'),
        'date': datetime.date(2016, 10, 10),
        'description': 'Commonplace',
        'notes': '',
        'supplement': [
            ('Original Description', 'COMMONPLACE COFFEE HOUSE')
        ]
    }

    assert actual == expected


def test_parse_refund():
    actual = mint.parse_transaction({
        'Account Name': 'CREDIT CARD',
        'Amount': '2.50',
        'Category': 'ATM Refund',
        'Date': '10/10/2016',
        'Description': 'ATM Refund',
        'Labels': '',
        'Notes': '',
        'Original Description': 'ATM REFUND',
        'Transaction Type': 'credit'
    })

    expected = {
        'account': 'CREDIT CARD',
        'amount': Decimal('2.50'),
        'date': datetime.date(2016, 10, 10),
        'description': 'ATM Refund',
        'notes': '',
        'supplement': [
            ('Original Description', 'ATM REFUND')
        ]
    }

    assert actual == expected


def test_get_data():
    actual = mint.get_data('tests/data/mint_transactions_basic.csv')
    expected = [
        {
            'account': 'CREDIT CARD',
            'amount': Decimal('-1250.00'),
            'date': datetime.date(2016, 10, 10),
            'description': 'Example Description',
            'notes': '',
            'supplement': [
                ('Original Description', 'FULL DESCRIPTION'),
            ]
        },
        {
            'account': 'CHECKING',
            'amount': Decimal('-5.00'),
            'date': datetime.date(2011, 4, 7),
            'description': 'Xxxxxxx Xxxxxxxxxxx Xxx',
            'notes': '',
            'supplement': [
                ('Original Description', 'XXXXXXX XXXXXXX XXX'),
            ]
        },
        {
            'account': 'CREDIT CARD',
            'amount': Decimal('-50.57'),
            'date': datetime.date(2011, 4, 8),
            'description': 'Xxxxxx',
            'notes': '',
            'supplement': [
                ('Original Description', 'XXXXXX 1231231231'),
            ]
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
