import datetime
from ledgertools import mint
from .utils import load_data


test_mint_data = 'tests/data/example_mint_transactions.csv'
parsed_data = 'tests/data/parsed_mint_data.pickle'
pend_trans_removed_data = 'tests/data/pending_trans_removed.pickle'


def test_parse_trans():
    actual = mint.parse_transaction({'date': '1/01/2017',
                                     'amount': '10.00',
                                     'other': 'stays the same'})
    expected = {'date': datetime.date(2017, 1, 1),
                'amount': '10.00',
                'other': 'stays the same'}

    assert actual == expected


def test_get_data():
    actual = mint.get_data(test_mint_data)
    expected = load_data(parsed_data)

    assert actual == expected


def test_pending_filter():
    actual = mint.filter_pending_trans(mint.get_data(test_mint_data))
    expected = load_data(pend_trans_removed_data)

    assert actual == expected
