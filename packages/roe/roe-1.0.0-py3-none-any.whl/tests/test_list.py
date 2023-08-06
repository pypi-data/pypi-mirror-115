from click.testing import CliRunner
from docker import APIClient
from docker.utils import kwargs_from_env

from roe.commands import cmd_deploy, cmd_undeploy
from roe.commands.cmd_list import cli
from roe.utilities import errors


def test_list_nonlocal():
    """
    Tests that not passing the local flag tells one to contact ChainOpt support.
    """
    runner = CliRunner()
    result = runner.invoke(cli)
    assert isinstance(result.exception, errors.NoLocalFlagError)
    assert "contact@chainopt.com" in result.output


def test_list_deployed():
    """
    Tests when a package is deployed to ensure that it's name is in the output
    """
    runner = CliRunner()
    runner.invoke(cmd_deploy.cli, ["-l", "-q", r"samples/myProject"])
    result = runner.invoke(cli, "-l")
    assert not result.exception
    assert "myProject" in result.output


def test_list_no_deployed():
    """
    Tests when there are no deployed packages and ensures that it says nothing
    """
    runner = CliRunner()
    runner.invoke(cmd_undeploy.cli, ["-l", "--all"], input="y\n")
    result = runner.invoke(cli, "-l")
    assert not result.exception
    assert "No packages deployed." in result.output


def test_list_limited_info():
    """ Tests when a package exists but the container does not """
    runner = CliRunner()
    runner.invoke(cmd_deploy.cli, ["-l", "-q", r"./samples/myProject"])

    # Delete container without removing package
    client = APIClient(**kwargs_from_env())
    myContainers = client.containers(all=True)
    for i in myContainers:
        if i['Names'][0] == r"/myProject":
            client.remove_container(container=i, force=True)

    result = runner.invoke(cli, "-l")
    runner.invoke(cmd_undeploy.cli, ["-l", "-p", "myProject"], input="y\n")
    assert not result.exception
    assert "Note: Showing limited information" in result.output
