import inspect
import os

settings_path = os.path.expanduser('~/.config/ledger_tools/settings.py')
settings = {
    'MINT_ACCOUNT_OVERRIDES': {}
}


def get_settings_from_module(module):
    '''https://github.com/getpelican/pelican/blob/master/pelican/settings.py'''

    if module is not None:
        settings.update(
                (k, v) for k, v in inspect.getmembers(module) if k.isupper()
        )

    return settings
