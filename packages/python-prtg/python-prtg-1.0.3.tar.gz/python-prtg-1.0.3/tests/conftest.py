import pytest

from python_prtg import writers


@pytest.fixture
def xml_writer() -> writers.XmlWriter:
    return writers.XmlWriter('/dev/null')


@pytest.fixture
def json_writer() -> writers.JsonWriter:
    return writers.JsonWriter('/dev/null')
