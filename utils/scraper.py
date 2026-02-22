import os
import re
import logging
import requests

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
        unique_links = list(dict.fromkeys(link for link in links if link.endswith(".html")))[:5]
        
        logger.info(f"Collected {len(unique_links)} unique article links.")
        return unique_links
    except TimeoutException:
        logger.error("Timed out waiting for article links to load.")
        return []

def scrape_article(driver, link):
    """Scrapes the title, content, and main image URL from a given article link."""
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

    try:
        title = driver.find_element(By.TAG_NAME, "h1").text.strip()
    except Exception:
        title = "Title not found"

    try:
        paragraphs = driver.find_elements(By.CSS_SELECTOR, "article p")
        content = " ".join([p.text for p in paragraphs if p.text.strip()])
    except Exception:
        content = ""

    try:
        image_element = driver.find_element(By.CSS_SELECTOR, "article img")
        image_url = image_element.get_attribute("src")
    except Exception:
        image_url = None
        logger.info("No image found for this article.")

    return title, content, image_url

def download_image(image_url, title, folder="images"):
    """Downloads an image from a URL and saves it based on the article title."""
    if not image_url:
        logger.info("Skipping download, no image URL provided.")
        return

    os.makedirs(folder, exist_ok=True)
    
    safe_title = re.sub(r"\W+", "_", title.lower()) if title != "Title not found" else "article_image"
    image_path = os.path.join(folder, f"{safe_title}.jpg")

    try:
        img_data = requests.get(image_url, timeout=10).content
        with open(image_path, "wb") as handler:
            handler.write(img_data)
        logger.info(f"Image saved to {image_path}")
    except requests.exceptions.RequestException as e:
        logger.warning(f"Failed to download image from {image_url}: {e}")
