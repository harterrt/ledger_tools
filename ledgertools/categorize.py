from functional import seq
from collections import Counter
from fuzzywuzzy import fuzz
from .utils import dump_amount
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import numpy as np
import pick
import pickle
import textwrap
from . import ledger

CATEGORIES = {
    'Expenses:Discretionary': 'd',
    'Expenses:Discretionary:Vacations': 'V',
    'Expenses:Food:Eating Out': 'e',
    'Expenses:Food:Groceries': 'g',
    'Expenses:Incedentals': 'n',
    'Expenses:Incedentals:Household': 'h',
    'Expenses:Incedentals:Household:Utilities': 'u',
    'Expenses:Discretionary:Recurring': 'r',
    'Expenses:Auto': 'c',
    'Liabilities:Mortgage': 'm',
    'Expenses:Discretionary:Amazon': 'a',
    'Expenses:Stipend': 's',
    'Income': 'i',
    'Ignore:Transfer': 't',
    'Receivables': 'b',
    'Assets:Vanguard': 'v',
    'Unknown': '?',
    'Expenses:Discretionary:Charitable': 'C',
}


def to_ledger_format(mint_tran, category):
    return textwrap.dedent("""\
        {date}  {description}
            ; {notes}
            {new_category}  {new_amount}
            {account}  {existing_amount}

        """).format(
            new_category=category,
            new_amount=dump_amount(-1 * mint_tran['amount']),
            existing_amount=dump_amount(mint_tran['amount']),
            **mint_tran
        )


def run_categorization(trans_path, ledger_path, out_path):
    success = True

    with open(trans_path, 'rb') as infile:
        trans = sorted(pickle.load(infile), key=lambda x: abs(x['amount']))

    def value(trans):
        return(
            seq(trans)
            .map(lambda x: abs(x['amount']))
            .sum()
        )

    total_trans = len(trans)
    total_value = value(trans)

    while success:
        tran = trans.pop()
        result = categorize(
            tran,
            {
                'current': total_trans - len(trans),
                'total': total_trans,
                'value': total_value - value(trans),
                'total_value': total_value,
            }
        )[0]

        if result is not None:
            # Save categorized transaction
            with open(out_path, 'a') as outfile:
                outfile.write(to_ledger_format(tran, result))

            # Save our progress
            with open(trans_path, 'wb') as outfile:
                pickle.dump(trans, outfile)
        else:
            success = False


def merge_dicts(*dict_args):
    """
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    https://stackoverflow.com/questions/38987/how-to-merge-two-python-dictionaries-in-a-single-expression
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result


def categorize(transaction, progress):
    display_params = merge_dicts(transaction, progress)

    title = textwrap.dedent("""\
        Transaction
        ===========
        Description : {description}
        Date        : {date}
        Amount      : {amount}
        Account     : {account}
        Notes       : {notes}
        Supplement  : {supplement}
        Progress    : {current} / {total}
        Value Prog  : {value:,.0f} / {total_value:,.0f}
        """).format(**display_params)

    picker = pick.Picker(
        CATEGORIES.keys(),
        title,
        options_map_func = format_category
    )

    # Register custom handlers
    # picker.register_custom_handler(ord('/'), pick_search)

    for key, value in CATEGORIES.items():
        picker.register_custom_handler(ord(value), choose_value(key))

    return picker.start()


def format_category(category):
    return('[{0}] - {1}'.format(CATEGORIES[category], category))


def choose_value(value):
    return(lambda picker: (value, -1))

def pick_search(picker):
    exit_chars = [27, ord('\n')]  # 27 is escape
    search_string = ''

    # There's probably a more elegant recursive method here
    # but I'm hacking today
    while True:
        picker.draw()
        c = picker.screen.getch()

        if c in exit_chars:
            return None
        else:
            search_string += chr(c)
            picker.options = fuzzy_order(picker.options, search_string)


def fuzzy_order(options, search_string):
    def key_func(option):
        return -fuzz.partial_ratio(option.lower(), search_string.lower())

    return (
        seq(options)
        .sorted(key=key_func)
        .list()
    )
