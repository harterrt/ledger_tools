# Ledger Tools

This is a suite of tools for adding new transactions to
[ledger](http://ledger-cli.org/) files.

## Workflow

Download a set of transactions from a financial aggregator.
This command only prints some helpful instructions for now:

```bash
python3 -m ledgertools.cli pull_mint
```

Then identify transactions that do not yet exist in a given ledger file.
Save these transactions to a temporary `new.pickle` file.

```bash
python3 -m ledgertools.cli dump_new_trans \
  --mint ~/Downloads/transactions.csv \
  --ledger ~/Private/account_data/.combined \
  --out ~/Private/account_data/new.pickle
```

Finally, categorize the new transactions one-by-one using a CLI:

```bash
python3 -m ledgertools.cli categorize \
  --new ~/Private/account_data/new.pickle \
  --ledger ~/Private/account_data/.combined \
  --out ~/Private/account_data/new.ledger
```

# What is Categorization?

Every transaction is posted to at lease two accounts.
Usually, one of the accounts is implied by the source data.
For example, all transactions downloaded from your checking account
should be posted against:

* an account representing you checking account (implied)
* some other account or virtual account (e.g. Expenses:Gas or Assets:Savings)

The categorization command will prompt the user with a new transaction
and a list of all existing accounts in the given ledger account.
This allows you to quickly find existing accounts
to post this transaction against.

## Categorization Actions

By default,
the categories are listed by frequency which is easy but not very useful.
We provide some additional actions to help you categorize faster:

* You can type '/' to enter fuzzy search mode.
  The categories will be reordered to best match your query.
* Typing 'b' will train a naive bayes classifier
  and reorder the categories based on their match liklihood.

# Transaction Type

All source plugins must return a list of *incomplete transactions*.
with exactly one account missing.
The incomplete transactions must have the following fields:

* `date` - `datetime.date`
* `description` - `string`
* `account` - `string`
* `amount` - `int` representing cents
* `notes` - `string`
* `supplement` - a `list` of `(string, string)` values
   to add context when categorizing


# Roadmap

For the foreseeable future, this project will focus on usability and reliability.

I'd like to break both the new transaction ingestion and categorization code
so they accept generic user plugins.
This would allow us to move away from Mint and towards open source scrapers or APIs.
