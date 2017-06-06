import datetime
from ledgertools.transaction import Transaction


new_transactions = [
    Transaction(
        account_name = 'CREDIT CARD',
        amount = '10.00',
        category = 'Gas & Fuel',
        date = datetime.date(2011, 4, 10),
        description = 'New Tran Description',
        labels = '',
        notes = '',
        original_description = 'Orig desc',
        transaction_type = 'debit'
    )
]


many_new_transactions = [
    Transaction(
        account_name = 'CREDIT CARD',
        amount = '10.00',
        category = 'Gas & Fuel',
        date = datetime.date(2011, 4, 10),
        description = 'New Tran Description',
        labels = '',
        notes = '',
        original_description = 'Orig desc',
        transaction_type = 'debit'
    ),
    Transaction(
        account_name = 'CREDIT CARD',
        amount = '50.00',
        category = 'Gas & Fuel',
        date = datetime.date(2011, 4, 10),
        description = 'New Tran Description',
        labels = '',
        notes = '',
        original_description = 'Orig desc',
        transaction_type = 'debit'
    ),
    Transaction(
        account_name = 'CREDIT CARD',
        amount = '67.00',
        category = 'Gas & Fuel',
        date = datetime.date(2011, 4, 10),
        description = 'New Tran Description',
        labels = '',
        notes = '',
        original_description = 'Orig desc',
        transaction_type = 'debit'
    )
]
