from csv import DictReader
import logging
import datetime


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

def filter_pending_trans(trans_list):
    """Remove pending transactions, since their amount may still change
    
    We pull data in ascending date format, but pending transactions are always
    at the top of the CSV file. Accordingly, we just need to remove all trans
    that are not in ascending order.
    """
    # Get next transaction - current transaction for every transaction
    # except last
    dates = list(map(lambda xx: xx['date'], trans_list))
    date_delta = map(lambda xx: xx[0] - xx[1], zip(dates[1:], dates[:-1]))

    # Find the big gap, if it exists
    year_gap = list(map(lambda xx: xx < datetime.timedelta(-1, 0, 0),
                        date_delta))
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

    print(critical_point)
    return trans_list[critical_point:]

