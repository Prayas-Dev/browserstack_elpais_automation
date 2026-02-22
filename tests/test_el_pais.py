import sys
import os
import pytest
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import run_test_logic

@pytest.mark.flaky(reruns=1, reruns_delay=2)
def test_el_pais_opinion_flow(driver):
    """
    Runs the full scrape->translate->analyze flow using the driver fixture
    provided by pytest-selenium, which will be a BrowserStack driver when
    run with the BrowserStack plugin.
    """
    try:
        run_test_logic(driver)
        # Mark test as passed on BrowserStack
        arguments = {"status": "passed", "reason": "Assertions passed"}
        script = f'browserstack_executor: {json.dumps({"action": "setSessionStatus", "arguments": arguments})}'
        driver.execute_script(script)
    except Exception as e:
        # Mark test as failed on BrowserStack
        error_message = f"An exception occurred: {str(e)}"
        arguments = {"status": "failed", "reason": error_message}
        script = f'browserstack_executor: {json.dumps({"action": "setSessionStatus", "arguments": arguments})}'
        driver.execute_script(script)
        pytest.fail(f"An exception occurred during the test: {e}")
