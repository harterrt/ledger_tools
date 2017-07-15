import textwrap
import datetime
from decimal import Decimal
from ledgertools.categorize import to_ledger_format


def test_to_ledger_format():
    mint_tran = {
            'account': 'CREDIT CARD',
            'amount': Decimal('-10.00'),
            'date': datetime.date(2011, 4, 8),
            'description': 'Xxxxxx',
            'notes': 'optional notes',
            'supplement': [
                ('original description', 'Orig desc'),
            ]
        }

    expected = textwrap.dedent("""\
        2011-04-08  Xxxxxx
            ; optional notes
            Expenses:Food:Eating Out  $10.00
            CREDIT CARD  $-10.00

        """)

    actual = to_ledger_format(mint_tran, 'Expenses:Food:Eating Out')

    assert actual == expected
