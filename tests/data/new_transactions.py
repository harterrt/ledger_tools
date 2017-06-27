import datetime


new_transactions = [
    {
        'account': 'CREDIT CARD',
        'amount': -1000,
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
        'amount': -1000,
        'date': datetime.date(2011, 4, 10),
        'description': 'New Tran Description',
        'notes': '',
        'supplement': [
            ('Original Description', 'Orig desc'),
        ]
    },
    {
        'account': 'CREDIT CARD',
        'amount': -5000,
        'date': datetime.date(2011, 4, 10),
        'description': 'New Tran Description',
        'notes': '',
        'supplement': [
            ('Original Description', 'Orig desc'),
        ]
    },
    {
        'account': 'CREDIT CARD',
        'amount': -6700,
        'date': datetime.date(2011, 4, 10),
        'description': 'New Tran Description',
        'notes': '',
        'supplement': [
            ('Original Description', 'Orig desc'),
        ]
    }
]
