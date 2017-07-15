import datetime
from decimal import Decimal


parsed_ledger_data = [
    {
        'amount': Decimal('50.57'),
        'category': 'Expenses:Food:Eating Out',
        'date': datetime.date(2011, 4, 8),
        'notes': ' None',
        'payee': 'Xxxxxx',
        'pending': '',
        'unit': '$',
        'unknown': ''
    },
    {
        'amount': Decimal('-50.57'),
        'category': 'CREDIT CARD',
        'date': datetime.date(2011, 4, 8),
        'notes': ' None',
        'payee': 'Xxxxxx',
        'pending': '',
        'unit': '$',
        'unknown': ''
    },
    {
        'amount': Decimal('5.00'),
        'category': 'Expenses:Incedentals:Gotchas',
        'date': datetime.date(2011, 4, 7),
        'notes': ' None',
        'payee': 'Xxxxxxx Xxxxxxxxxxx Xxx',
        'pending': '',
        'unit': '$',
        'unknown': ''
    },
    {
        'amount': Decimal('-5.00'),
        'category': 'CHECKING',
        'date': datetime.date(2011, 4, 7),
        'notes': ' None',
        'payee': 'Xxxxxxx Xxxxxxxxxxx Xxx',
        'pending': '',
        'unit': '$',
        'unknown': ''
    },
    {
        'amount': Decimal('60.57'),
        'category': 'Expenses:Transport:Gas',
        'date': datetime.date(2011, 4, 8),
        'notes': ' None',
        'payee': 'Xxxxxx',
        'pending': '',
        'unit': '$',
        'unknown': ''
    },
    {
        'amount': Decimal('-60.57'),
        'category': 'CREDIT CARD',
        'date': datetime.date(2011, 4, 8),
        'notes': ' None',
        'payee': 'Xxxxxx',
        'pending': '',
        'unit': '$',
        'unknown': ''
    }]
