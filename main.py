import sys
import os
from dotenv import load_dotenv
from selenium import webdriver

# Add project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from utils.scraper import get_opinion_articles, scrape_article, download_image
from utils.translator import translate_text
from utils.analyzer import find_repeated_words

def run_test_logic(driver):
    """
    Main function to scrape, analyze, and report on El País opinion articles.
    """
    links = get_opinion_articles(driver)

    if not links or len(links) < 5:
        print("Failed to retrieve the expected number of article links. Exiting.")
        return

    translated_titles = []
    for link in links:
        title, content, image_url = scrape_article(driver, link)

        if title and content:
            print("\n--- ARTICLE ---")
            print(f"Title (Spanish): {title}")

            translated_title = translate_text(title)
            print(f"Translated Title: {translated_title}")
            translated_titles.append(translated_title)
            
            print(f"Content (Spanish, excerpt): {content[:200]}...")
            
            download_image(image_url, title)
        else:
            print(f"\n--- SKIPPING ARTICLE ---")
            print(f"Failed to scrape article or content for link: {link}. Moving to next.")

    # Analyze repeated words across translated headers (as per assignment)
    combined_headers = " ".join(translated_titles)
    print("\n--- ANALYSIS (words repeated more than twice across translated headers) ---")
    repeated_words = find_repeated_words(combined_headers, min_count=3, stopwords="en")

    if repeated_words:
        for word, count in repeated_words.items():
            print(f"- {word}: {count} times")
    else:
        print("No words appeared frequently enough for analysis.")

def main():
    load_dotenv()
    driver = None
    try:
        driver = webdriver.Chrome()
        driver.set_page_load_timeout(60)
        driver.maximize_window()
        run_test_logic(driver)
    finally:
        if driver:
            driver.quit()
            print("\nExecution finished and browser closed.")

if __name__ == "__main__":
    main()
