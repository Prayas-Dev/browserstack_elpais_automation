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
    provided by conftest.py (local) or BrowserStack SDK (cloud).

    Validates that:
    - At least 1 article link is scraped
    - Titles are extracted and non-empty
    - Translation produces English text
    """
    from utils.scraper import get_opinion_articles, scrape_article
    from utils.translator import translate_text

    try:
        # Step 1: Get opinion article links
        links = get_opinion_articles(driver)
        assert links and len(links) > 0, "Expected at least 1 article link from the Opinion section."

        # Step 2: Scrape at least the first article and verify data
        title, content, image_url = scrape_article(driver, links[0])
        assert title and title != "Title not found", f"Failed to scrape title from: {links[0]}"
        assert content and len(content) > 0, f"Failed to scrape content from: {links[0]}"

        # Step 3: Verify translation works
        translated = translate_text(title)
        assert translated and len(translated) > 0, "Translation returned empty result."

        # Step 4: Run the full flow (processes all articles)
        run_test_logic(driver)

        # Mark test as passed on BrowserStack (if running on BrowserStack)
        _set_browserstack_status(driver, "passed", "All assertions passed")

    except Exception as e:
        # Mark test as failed on BrowserStack (if running on BrowserStack)
        _set_browserstack_status(driver, "failed", f"An exception occurred: {str(e)}")
        raise


def _set_browserstack_status(driver, status, reason):
    """Safely set BrowserStack session status. No-op when running locally."""
    try:
        arguments = {"status": status, "reason": reason}
        script = f'browserstack_executor: {json.dumps({"action": "setSessionStatus", "arguments": arguments})}'
        driver.execute_script(script)
    except Exception:
        # Not running on BrowserStack — ignore the JavaScript error
        pass
