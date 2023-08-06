import os

from roe.utilities import utils


def test_bad_yaml_load():
    """ Tests when a poorly configured YAML file is given. """
    filename = "bad.yaml"
    with open(filename, "w") as bad_yaml:
        bad_yaml.write("aaslvclk:fjas;lk:jflask:klsfdj:\n\n\n:fkdlj")
        bad_yaml.close()
    result = utils.load_yaml(os.path.join(os.getcwd(), filename))

    os.remove(filename)
    assert result is None


def test_check_port_good():
    port = 65000
    result = utils.check_port(port)
    assert result == port
