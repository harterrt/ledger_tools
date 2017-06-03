from functional import seq
from collections import Counter
from pick import pick
import pickle
import textwrap
from . import ledger


def run_categorization(trans_path):
    with open(trans_path, 'r') as infile:
        trans = pickle.load(infile)

    categorize(trans.pop())

    with open(trans_path, 'w') as outfile:
        pickle.dump(trans, outfile)


def get_category_frequencies(ledger_path):
    return seq(ledger.get_transactions(ledger_path))\
        .map(lambda x: Counter([x['category']]))\
        .reduce(lambda x, y: x + y)\
        .most_common()


def categorize(transaction, ledger_path):
    title = textwrap.dedent("""\
        Transaction
        ===========
        Description : {description}
        Date        : {date}
        Amount      : {amount}
        Account     : {account name}
        Notes       : {notes}
        """).format(**transaction)

    categories = get_category_frequencies(ledger_path)
    pick(categories, title)
