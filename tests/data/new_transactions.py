from decimal import Decimal
import datetime


new_transactions = [
    {
        'account': 'CREDIT CARD',
        'amount': Decimal('-10.00'),
        'date': datetime.date(2011, 4, 10),
        'description': 'New Tran Description',
        'notes': '',
        'supplement': [
            ('Original Description', 'Orig desc'),
        ]
    }
]


many_new_transactions = [
    {
        'account': 'CREDIT CARD',
        'amount': Decimal('-10.00'),
        'date': datetime.date(2011, 4, 10),
        'description': 'New Tran Description',
        'notes': '',
        'supplement': [
            ('Original Description', 'Orig desc'),
        ]
    },
    {
        'account': 'CREDIT CARD',
        'amount': Decimal('-50.00'),
        'date': datetime.date(2011, 4, 10),
        'description': 'New Tran Description',
        'notes': '',
        'supplement': [
            ('Original Description', 'Orig desc'),
        ]
    },
    {
        'account': 'CREDIT CARD',
        'amount': Decimal('-67.00'),
        'date': datetime.date(2011, 4, 10),
        'description': 'Check #102',
        'notes': '',
        'supplement': [
            ('Original Description', 'Orig desc'),
        ]
    }
]
