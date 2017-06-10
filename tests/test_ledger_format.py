import textwrap
import datetime
from ledgertools.categorize import to_ledger_format


def test_to_ledger_format():
    mint_tran = {
            'account name': 'CREDIT CARD',
            'amount': '10.00',
            'category': 'Gas & Fuel',
            'date': datetime.date(2011, 4, 8),
            'description': 'Xxxxxx',
            'labels': '',
            'notes': 'optional notes',
            'original description': 'Orig desc',
            'transaction type': 'debit'
        }

    expected = textwrap.dedent("""\
        2011-04-08  Xxxxxx
            ; optional notes
            Expenses:Food:Eating Out  $10.00
            CREDIT CARD

        """)

    actual = to_ledger_format(mint_tran, 'Expenses:Food:Eating Out')

    assert actual == expected
