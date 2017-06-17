import click
from . import data_actions
from . import categorize as cat
import pickle


@click.group()
def cli():
    pass


@cli.command()
def pull_mint():
    click.echo("Log into mint, then go to the following address:\n"
               "https://wwws.mint.com/transactionDownload.event?"
               "queryNew=&offset=0&filterType=cash&comparableType=4"
               "\n\n"
               "Then copy the file to your working dir")


@cli.command()
@click.option('--mint', help='Path to mint transaction data.',
              type=click.Path(exists=True), required=True)
@click.option('--ledger', help='Path to current ledger file.',
              type=click.Path(exists=True), required=True)
@click.option('--out', help='Path to save the new tranasactions.',
              type=click.Path(), required=True)
def dump_new_trans(mint, ledger, out):
    new = data_actions.new_trans_from_path(mint, ledger)

    with open(out, 'wb') as outfile:
        pickle.dump(new, outfile)


@cli.command()
@click.option('--new',
              help='Path to new transactions, as created by `dump_new_trans`')
@click.option('--ledger',
              help='Path to save resulting ledger transactions')
@click.option('--out',
              help='Path to save resulting ledger transactions')
def categorize(new, ledger, out):
    cat.run_categorization(new, ledger, out)


if __name__ == "__main__":
    cli()
