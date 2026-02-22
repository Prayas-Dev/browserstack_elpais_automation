import pytest

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="browser to run tests on")

@pytest.fixture
def driver(request):
    # This is a placeholder fixture.
    # The actual driver will be injected by pytest-selenium or pytest-browserstack.
    return request.getfixturevalue("driver")
