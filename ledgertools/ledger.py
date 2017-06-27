from subprocess import check_output
from .utils import parse_amount
import datetime
from io import StringIO
import csv


def ledger_to_csv(path):
    return check_output(['ledger', '-f', path, 'csv'])


def get_transactions(ledger_path):
    # TODO: Make this more testable
    bstring = ledger_to_csv(ledger_path)
    transactions = bstring.decode('utf8')

    split_trans = list(csv.reader(StringIO(transactions)))

    return list(map(parse_transaction, split_trans))


def parse_transaction(tran):
    headers = [
        'date',
        'unknown',
        'payee',
        'category',
        'unit',
        'amount',
        'pending',
        'notes',
    ]
    trans_dict = dict(zip(headers, tran))

    modifiers = {
        'date': lambda x: datetime.datetime.strptime(x, "%Y/%m/%d").date(),
        # TODO: maybe use a named tuple with dollars and cents?
        #       better than a int of cents, since you won't forget to render
        #       later
        'amount': parse_amount
    }
    return {k: modifiers.get(k, lambda x: x)(v)
            for (k, v)
            in trans_dict.items()}
