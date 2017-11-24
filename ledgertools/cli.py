import click
import pickle
from importlib.machinery import SourceFileLoader
from . import data_actions
from . import categorize as cat


def get_settings_from_module(module):
    '''https://github.com/getpelican/pelican/blob/master/pelican/settings.py#L212'''

    settings = {
        'MINT_ACCOUNT_OVERRIDES': {}
    }
    if module is not None:
        settings.update(
                (k, v) for k, v in inspect.getmembers(module) if k.isupper()
        )

    return settings

@click.group()
@click.option('--config', help='Path to ledger config file.',
              type=click.Path(exists=True),
              default='~/.config/ledger_tools/config')
@click.pass_context
def cli(ctx, config_path):
    try:
        module = SourceFileLoader('lt_config', config_path).load_module())
    except e:
        module = None
        click.echo(
            "Couldn't load config file %s: %s".format(config_path, e.msg)
        )

    ctx.obj['config'] = get_settings_from_module(module)


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
@click.pass_context
def dump_new_trans(ctx, mint, ledger, out):
    overrides = ctx.obj.get('MINT_ACCOUNT_OVERRIDES', {})
    new = data_actions.new_trans_from_path(mint, ledger, overrides)

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
