from csv import DictReader
import logging
import datetime

import pickle


def get_data(path='~/Private/account_data/mint_transactions.csv'):
    with open(path, 'r') as infile:
        trans = [parse_transaction(tt) for tt in DictReader(infile)]

    return trans

def parse_transaction(tran):
    """Clean headers and parse values"""

    modifiers = {
        'date': lambda dd: datetime.datetime.strptime(dd, '%m/%d/%Y').date(),
        'amount': float
    }

    def clean_field(field):
        """Map key to lowercase and clean value if function specified"""
        key = field[0].lower()
        value = modifiers.get(key, lambda x: x)(field[1])
        
        return key, value

    return dict(map(clean_field, tran.items()))

def tail(iterable):
    iterable.__next__()
    return iterable

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
        raise PendingTransactionException("More than one pending breakpoints")
    elif (sum(year_gap) == 0):
        logging.info("No pending transactions found.")
        critical_point = 0
    else:
        critical_point = year_gap.index(True) + 1
        logging.info("%d pending transactions removed.", critical_point)

    return trans_list[critical_point:]

def __pickle__(obj, path):
    with open(path, 'wb') as outfile:
        pickle.dump(obj, outfile)

