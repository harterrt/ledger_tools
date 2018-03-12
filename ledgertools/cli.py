import click
import pickle
import os
from importlib.machinery import SourceFileLoader
from . import config
from . import data_actions
from . import categorize as cat


def settings_option(func):
    def callback(ctx, param, settings_path):
        try:
            module = SourceFileLoader('lt_config', settings_path).load_module()
        except FileNotFoundError as e:
            module = None
            click.echo(
                "Couldn't load config file {}: {}".format(settings_path, e.strerror)
            )

        return config.get_settings_from_module(module)

    return click.option('--settings', help='Path to ledger settings file.',
                        type=click.Path(), callback=callback,
                        default=config.settings_path)(func)


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
@settings_option
def dump_new_trans(mint, ledger, out, settings):
    print("Test")
    print(settings)
    print(config.settings)
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
@settings_option
def categorize(new, ledger, out, settings):
    cat.run_categorization(new, ledger, out)


if __name__ == "__main__":
    cli()
