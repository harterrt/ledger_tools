# Ledger Tools

This is a suite of tools for adding new transactions to
[ledger](http://ledger-cli.org/) files.

## Workflow

Download a set of transactions from a financial aggregator.
This command only prints some helpful instructions for now:

```bash
python -m ledgertools.cli pull_mint
```

Then identify transactions that do not yet exist in a given ledger file.
Save these transactions to a temporary `new.pickle` file.

```bash
python -m ledgertools.cli dump_new_trans \
  --mint ~/Downloads/transactions.csv \
  --ledger ~/Private/account_data/.combined \
  --out ~/Private/account_data/new.pickle
```

Finally, categorize the new transactions one-by-one using a CLI:

```bash
python -m ledgertools.cli dump_new_trans \
  --new ~/Private/account_data/new.pickle \
  --ledger ~/Private/account_data/.combined \
  --out ~/Private/account_data/new.ledger
```

This command will prompt the user with a new transaction
and a list of all existing categories from the given ledger account.
This allows you to quickly find existing accounts to post this transaction against.

By default, the categories are listed by frequency which is easy but not very useful.

## Categorization Actions

* You can type '/' to enter fuzzy search mode.
  The categories will be reordered to best match your query.

# Roadmap

For the foreseeable future, this project will focus on usability and reliability.

I'd like to break both the new transaction ingestion and categorization code
so they accept generic user plugins.
This would allow us to move away from Mint and towards open source scrapers or APIs.
