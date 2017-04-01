from ledger_tools import mint, ledger


def render_new_trans(mint_file, ledger_file):
    """Stub function for finding new mint transactions"""
    mint_trans = mint.filter_pending_trans(mint.get_data(mint_file))
    ledger_trans = ledger.read_ledger_trans(ledger_file)

    return render(diff(mint_trans, ledger_trans))
