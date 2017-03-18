from subprocess import check_output
from io import StringIO
import csv

def ledger_to_csv(path):
    return check_output(['ledger', '-f', ledger_path, 'csv'])

def get_transactions(ledger_path):
    # TODO: Make this more testable
    bstring = ledger_to_csv(ledger_path)
    transactions = bstring.decode('utf8')

    split_trans = list(csv.reader(StringIO(transactions)))

    return list(map(parse_transaction, split_trans))


def parse_transaction(tran):
    pass
