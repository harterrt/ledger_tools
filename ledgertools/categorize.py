from functional import seq
from collections import Counter
import pick
import pickle
import textwrap
from . import ledger


def to_ledger_format(mint_tran, category):
    return textwrap.dedent("""\
        {date}  {description}
            ; {notes}
            {new_category}  ${amount}
            {account name}
        """).format(new_category=category, **mint_tran)


def run_categorization(trans_path, ledger_path, out_path):
    with open(trans_path, 'rb') as infile:
        trans = pickle.load(infile)

    tran = trans.pop()
    result = categorize(tran, ledger_path)[0]

    if result is not None:
        # Save categorized transaction
        with open(out_path, 'w') as outfile:
            outfile.write(to_ledger_format(tran, result))

        # Save our progress
        with open(trans_path, 'wb') as outfile:
            pickle.dump(trans, outfile)


def get_category_frequencies(ledger_trans):
    most_common = seq(ledger_trans)\
        .map(lambda x: Counter([x['category']]))\
        .reduce(lambda x, y: x + y)\
        .most_common()

    return [key for key, value in most_common]


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

    # Get all transactions with similar transaction type (debit/credit) from
    # ledger file
    ledger_trans = ledger.get_transactions(ledger_path)
    categories = get_category_frequencies(ledger_trans)
    return pick.pick(categories, title)
