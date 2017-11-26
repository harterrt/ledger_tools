from csv import DictReader
from .utils import parse_amount
import logging
import datetime


settings = {
}


def get_data(path):
    with open(path, 'r') as infile:
        trans = [parse_transaction(tt) for tt in DictReader(infile)]

    return trans


def parse_transaction(tran):
    # Convert raw transaction `tran` into an incomplete transaction

    # Amounts decrease asset accounts unless specified as a credit.
    amount_multiplier = 1 if tran['Transaction Type'] == 'credit' else -1

    # Account overrides - converts Mint's account names to ledger names
    overrides = settings.get('MINT_ACCOUNT_OVERRIDES', {})

    # Build incomplete transaction and return
    return {
        'date': datetime.datetime.strptime(tran['Date'], '%m/%d/%Y').date(),
        'description': tran['Description'],
        'account': overrides.get(tran['Account Name'], tran['Account Name']),
        'amount': parse_amount(tran['Amount']) * amount_multiplier,
        'notes': tran['Notes'],
        'supplement': [
            ('Original Description', tran['Original Description'])
        ]
    }


def filter_pending_trans(trans_list):
    """Remove pending transactions, since their amount may still change

    We pull data in ascending date format, but pending transactions are always
    at the top of the CSV file. Accordingly, we just need to remove all trans
    that are not in ascending order.
    """
    # Get next transaction - current transaction for every transaction
    # except last
    dates = [xx['date'] for xx in trans_list]
    date_delta = [xx[0] - xx[1] for xx in zip(dates[1:], dates)]

    # Find the big gap, if it exists
    year_gap = [xx < datetime.timedelta(-1, 0, 0) for xx in date_delta]

    if (sum(year_gap) > 1):
        logging.error("There are %d pending transaction breakpoints, " +
                      "when there should be no more than one.",
                      sum(year_gap))
        raise Exception("More than one pending breakpoints")
    elif (sum(year_gap) == 0):
        logging.info("No pending transactions found.")
        critical_point = 0
    else:
        critical_point = year_gap.index(True) + 1
        logging.info("%d pending transactions removed.", critical_point)

    return trans_list[critical_point:]


def get_transactions(mint_file):
    return filter_pending_trans(get_data(mint_file))
