from collections import namedtuple
import datetime


TransactionBase = namedtuple(
    'TransactionBase', 
    ['date', 'payee', 'notes', 'category', 'amount', 'labels']
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
        return cls(
            date = ledger_tran['date'],
            payee = ledger_tran['payee'],
            notes = ledger_tran['notes'],
            category = ledger_tran['category'],
            amount = ledger_tran['amount'],
            unit = ledger_tran['labels'],
        )

    def get_keyed_tran(self):
        return ((self.date, self.amount, self.description), self)
