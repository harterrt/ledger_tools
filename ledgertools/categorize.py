from functional import seq
from collections import Counter
from fuzzywuzzy import fuzz
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
    success = True

    with open(trans_path, 'rb') as infile:
        trans = pickle.load(infile)

    total_trans = len(trans)

    ledger_trans = ledger.get_transactions(ledger_path)

    while success:
        tran = trans.pop()
        result = categorize(
            tran,
            ledger_trans,
            {
                'current': total_trans - len(trans),
                'total': total_trans
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


def get_category_frequencies(ledger_trans):
    most_common = seq(ledger_trans)\
        .map(lambda x: Counter([x['category']]))\
        .reduce(lambda x, y: x + y)\
        .most_common()

    return [key for key, value in most_common]


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


def categorize(transaction, ledger_trans, progress):
    display_params = merge_dicts(transaction, progress)
    title = textwrap.dedent("""\
        Transaction
        ===========
        Description : {description} ({original description})
        Date        : {date}
        Amount      : {amount}
        Account     : {account name}
        Notes       : {notes}
        Progress    : {current} / {total}
        """).format(**display_params)

    categories = get_category_frequencies(ledger_trans)

    picker = pick.Picker(categories, title)

    # Register custom handlers
    picker.register_custom_handler(ord('/'), pick_search)

    return picker.start()


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

    return seq(options) \
        .sorted(key=key_func) \
        .list()
