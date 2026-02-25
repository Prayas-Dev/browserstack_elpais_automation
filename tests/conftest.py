import pytest
from selenium import webdriver


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="browser to run tests on")


@pytest.fixture
def driver(request):
    """
    Provides a Selenium WebDriver instance.
    When run via BrowserStack SDK, the SDK overrides this fixture with its own driver.
    When run locally, this creates a local Chrome driver.
    """
    browser = request.config.getoption("--browser").lower()

    if browser == "firefox":
        d = webdriver.Firefox()
    elif browser == "edge":
        d = webdriver.Edge()
    else:
        d = webdriver.Chrome()

    d.set_page_load_timeout(60)
    d.maximize_window()

    yield d

    d.quit()
