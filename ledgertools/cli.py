import click
from . import data_actions
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
@click.option('--mint', default='~/Downloads/transactions.csv',
              help='Path to mint transaction data.')
@click.option('--ledger', help='Path to current ledger file.')
@click.option('--out', help='Path to save the new tranasactions.')
def dump_new_trans(mint, ledger, out):
    new = data_actions.new_trans_from_paths(mint, ledger)

    with open(out, 'wb') as outfile:
        pickle.dump(new, outfile)


if __name__ == "__main__":
    cli()
