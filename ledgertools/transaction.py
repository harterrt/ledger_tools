from collections import namedtuple
import datetime


TransactionBase = namedtuple(
    'TransactionBase', 
    ['account_name', 'amount', 'category', 'date', 'description', 'labels',
     'notes', 'original_description', 'transaction_type']
)


def _to_date(datestr, fmt):
    return datetime.datetime.strptime(datestr, fmt).date()


class Transaction(TransactionBase):
    @classmethod
    def from_mint(cls, mint_tran):
        return cls(
            account_name = mint_tran['Account Name'],
            amount = mint_tran['Amount'],
            category = mint_tran['Category'],
            date = _to_date(mint_tran['Date'], '%m/%d/%Y'),
            description = mint_tran['Description'],
            labels = mint_tran['Labels'],
            notes = mint_tran['Notes'],
            original_description = mint_tran['Original Description'],
            transaction_type = mint_tran['Transaction Type']
        )


    @classmethod
    def from_ledger(cls, ledger_tran):
        pass
        #return super().__init__(
        #    account_name = mint_tran['account name'],
        #    amount = mint_trans['amount'],
        #    category = mint_tran['category'],
        #    date = mint_tran['date'],
        #    description = mint_tran['description'],
        #    labels = mint_tran['labels'],
        #    notes = mint_tran['notes'],
        #    original_description = mint_tran['original description'],
        #    transaction_type = mint_tran['transaction type']
        #)

    def get_keyed_tran(self):
        return ((self.date, self.amount, self.description), self)
