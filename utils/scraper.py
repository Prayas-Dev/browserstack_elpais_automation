import os
import re
import logging
import requests

from urllib.parse import urlparse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_opinion_articles(driver, url="https://elpais.com/opinion/"):
    """Navigates to the opinion section and returns the top 5 unique article links."""
    logger.info(f"Opening {url}")
    driver.get(url)
    wait = WebDriverWait(driver, 15)

    try:
        consent_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Accept') or contains(., 'Aceptar')]"))
        )
        consent_button.click()
        logger.info("Cookie popup handled.")
    except TimeoutException:
        logger.info("No cookie popup was detected or it timed out.")

    try:
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article h2 a")))
        articles = driver.find_elements(By.CSS_SELECTOR, "article h2 a")
        
        links = [article.get_attribute("href") for article in articles if article.get_attribute("href")]

        # Filter to actual article links (not anchors, fragments, or javascript links)
        def is_article_link(link):
            parsed = urlparse(link)
            return (
                parsed.scheme in ("http", "https")
                and "elpais.com" in parsed.netloc
                and parsed.path not in ("/", "")
            )

        unique_links = list(dict.fromkeys(link for link in links if is_article_link(link)))[:5]
        
        logger.info(f"Collected {len(unique_links)} unique article links.")
        return unique_links
    except TimeoutException:
        logger.error("Timed out waiting for article links to load.")
        return []

def scrape_article(driver, link):
    """Scrapes the title, content, and main image URL from a given article link.
    
    Handles paywalled articles gracefully by trying multiple selectors
    and falling back to any available visible text.
    """
    logger.info(f"Scraping article: {link}")
    try:
        driver.get(link)
    except TimeoutException:
        logger.error(f"Timed out while loading article: {link}. Skipping this article.")
        return None, None, None
    wait = WebDriverWait(driver, 15)

    try:
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "article")))
    except TimeoutException:
        logger.error("Article page did not load correctly.")
        return None, None, None

    # --- Extract title ---
    try:
        title = driver.find_element(By.TAG_NAME, "h1").text.strip()
    except Exception:
        title = "Title not found"

    # --- Extract content (paywall-resilient) ---
    content = ""
    # Try multiple selectors in order of specificity
    content_selectors = [
        "article .a_c p",                              # El País main article body
        "[data-dtm-region='articulo_cuerpo'] p",       # data attribute variant
        "article .article_body p",                     # generic article body
        "article p",                                   # broadest fallback
    ]
    for selector in content_selectors:
        try:
            paragraphs = driver.find_elements(By.CSS_SELECTOR, selector)
            text = " ".join([p.text for p in paragraphs if p.text.strip()])
            if text:
                content = text
                break
        except Exception:
            continue

    # If all paragraph selectors failed, try extracting any visible text from <article>
    if not content:
        try:
            article_el = driver.find_element(By.TAG_NAME, "article")
            raw_text = article_el.text.strip()
            # Remove the title from the raw text to avoid duplication
            if title and title != "Title not found" and raw_text.startswith(title):
                raw_text = raw_text[len(title):].strip()
            if raw_text:
                content = raw_text
                logger.info("Used fallback: extracted visible text from <article> element.")
        except Exception:
            pass

    if not content:
        logger.warning(f"No article content could be extracted (likely paywalled): {link}")

    # --- Extract image ---
    image_url = None
    try:
        image_elements = driver.find_elements(By.CSS_SELECTOR, "article img")
        for img in image_elements:
            src = img.get_attribute("src")
            if src and _is_valid_image_url(src):
                image_url = src
                break
        if not image_url:
            logger.info("No suitable image found for this article.")
    except Exception:
        logger.info("No image found for this article.")

    return title, content, image_url

def _is_valid_image_url(url):
    """Checks if a URL looks like a real article image (not a tracking pixel, data URI, or icon)."""
    if not url:
        return False
    if url.startswith("data:"):
        return False
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        return False
    # Skip tiny icons/tracking pixels by checking common image extensions or known CDN patterns
    path_lower = parsed.path.lower()
    skip_extensions = ('.svg', '.gif', '.ico')
    if any(path_lower.endswith(ext) for ext in skip_extensions):
        return False
    return True

def download_image(image_url, title, folder="images"):
    """Downloads an image from a URL and saves it based on the article title."""
    if not image_url:
        logger.info("Skipping download, no image URL provided.")
        return

    os.makedirs(folder, exist_ok=True)
    
    # Sanitize title for safe filename — replace ALL non-alphanumeric/underscore chars
    safe_title = re.sub(r"[^\w]", "_", title.lower(), flags=re.UNICODE) if title != "Title not found" else "article_image"
    # Collapse multiple underscores into one and strip trailing underscores
    safe_title = re.sub(r"_+", "_", safe_title).strip("_")
    image_path = os.path.join(folder, f"{safe_title}.jpg")

    try:
        img_data = requests.get(image_url, timeout=10).content
        with open(image_path, "wb") as handler:
            handler.write(img_data)
        logger.info(f"Image saved to {image_path}")
    except requests.exceptions.RequestException as e:
        logger.warning(f"Failed to download image from {image_url}: {e}")
