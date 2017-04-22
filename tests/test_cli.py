import pytest
from click.testing import CliRunner
from ledger_tools import cli


@pytest.fixture
def runner():
    return CliRunner()


def test_cli(runner):
    result = runner.invoke(cli.pull_mint)
    assert result.exit_code == 0
    assert not result.exception
    assert "mint.com" in result.output
