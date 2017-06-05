from click import getchar
from functional import seq
from collections import Counter
import pick
import pickle
import textwrap
from . import ledger


def run_categorization(trans_path, ledger_path, out_path):
    with open(trans_path, 'rb') as infile:
        trans = pickle.load(infile)

    print("="*80)

    result = categorize(trans.pop(), ledger_path)
    print('-'*80)
    print(result)
    print('-'*80)

    if result is not None:
        # Save categorized transaction
        with open(out_path, 'w') as outfile:
            outfile.write(result[0][0])

        print("!"*80)
        # Save our progress
        with open(trans_path, 'wb') as outfile:
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

    print(';'*80)
    categories = get_category_frequencies(ledger_path)
    print(']'*80)
    print(categories)
    print(title)
    print('['*80)
    picker = pick.Picker(categories, title)
    print('*'*80)
    out = picker.start()
    print('!'*80)
    print(out)
    print('['*80)
    return out
