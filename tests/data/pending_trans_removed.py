import datetime


pending_trans_removed = [
    {
        'account': 'CHECKING',
        'amount': -500,
        'date': datetime.date(2011, 4, 7),
        'description': 'Xxxxxxx Xxxxxxxxxxx Xxx',
        'notes': '',
        'supplement': [
            ('Original Description', 'XXXXXXX XXXXXXX XXX'),
        ]
    },
    {
        'account': 'CREDIT CARD',
        'amount': -5057,
        'date': datetime.date(2011, 4, 8),
        'description': 'Xxxxxx',
        'notes': '',
        'supplement': [
            ('Original Description', 'XXXXXX 1231231231'),
        ]
    },
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
