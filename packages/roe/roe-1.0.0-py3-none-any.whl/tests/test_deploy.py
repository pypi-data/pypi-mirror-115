from click.testing import CliRunner

from roe.commands import cmd_undeploy
from roe.commands.cmd_deploy import cli
from roe.utilities.errors import *


def test_deploy_no_package():
    """
    Tests if ROE properly gives an error if no package is given to deploy.
    """
    runner = CliRunner()
    result = runner.invoke(cli)
    assert isinstance(result.exception, SystemExit)
    assert result.exit_code == 2
    assert "Missing argument" in result.output


def test_deploy_nonlocal():
    """
    Tests that not passing the local flag tells one to contact ChainOpt support.
    """
    runner = CliRunner()
    result = runner.invoke(cli, [r"samples/myProject"], input="y\n")
    assert isinstance(result.exception, NoLocalFlagError)


def test_deploy_bad_package_path():
    """
    Tests error handling when passing through a bad package name.
    """
    runner = CliRunner()
    result = runner.invoke(cli, ["-l", "asdfljk"])
    assert isinstance(result.exception, PackagePathError)


def test_deploy_base():
    """ Base case for testing the deploy command"""
    runner = CliRunner()
    result = runner.invoke(cli, ["-l", r"samples/myProject"], input="y\n")
    assert not result.exception


def test_deploy_bad_port():
    runner = CliRunner()
    runner.invoke(cmd_undeploy.cli, ["-l", "--all"], input="y\n")
    result = runner.invoke(cli, ["-l", r"samples/myProject", "-p", "900"], input="y\n")
    assert isinstance(result.exception, BadPortError)
