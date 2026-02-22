# El País Article Scraper and Analyzer

This project automates the process of scraping articles from the Opinion section of El País (a Spanish news outlet), translating their titles to English, analyzing repeated words in the translated titles, and demonstrating cross-browser testing on BrowserStack.

## Features

*   Navigates to El País Opinion section and handles cookie consent.
*   Scrapes the first five unique articles, extracting title, content excerpt, and cover image URL.
*   Downloads cover images locally.
*   Translates article titles from Spanish to English using the RapidAPI Google Translate 113 API.
*   Analyzes translated English titles to identify words repeated more than twice, excluding common English stopwords.
*   Supports local execution.
*   Configured for cross-browser testing on BrowserStack across desktop and mobile platforms.

## Requirements

Before you begin, ensure you have met the following requirements:

*   **Python 3.8+**: The project is developed and tested with Python 3.x.
*   **pip**: Python package installer, usually comes with Python.
*   **BrowserStack Account**: Required for running tests on BrowserStack. You will need your `BROWSERSTACK_USERNAME` and `BROWSERSTACK_ACCESS_KEY`.
*   **RapidAPI Account (for Google Translate 113 API)**: Required for translation. You will need your `RAPIDAPI_KEY`.

## Setup Instructions

Follow these steps to get the project up and running on your local machine:

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/your-username/browserstack-assignment.git
    cd browserstack-assignment
    ```

2.  **Create and Activate a Virtual Environment:**
    It's recommended to use a virtual environment to manage project dependencies.
    ```bash
    python -m venv venv
    ```
    *   **On Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    *   **On macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**
    Create a `.env` file in the root directory of the project based on `.env.example`.
    ```
    BROWSERSTACK_USERNAME="YOUR_BROWSERSTACK_USERNAME"
    BROWSERSTACK_ACCESS_KEY="YOUR_BROWSERSTACK_ACCESS_KEY"
    RAPIDAPI_KEY="YOUR_RAPIDAPI_KEY"
    ```
    Replace the placeholder values with your actual credentials.

## How to Run Locally

To execute the scraping, translation, and analysis flow locally:

```bash
python main.py
```

The script will:
*   Open a Chrome browser instance.
*   Navigate to El País Opinion section.
*   Scrape and process the first five articles.
*   Print titles (Spanish), translated titles (English), and content excerpts.
*   Download cover images to the `images` folder.
*   Print an analysis of words repeated more than twice across translated headers.
*   Gracefully handle and report any articles that fail to load or scrape.

## How to Run on BrowserStack

To run the full test suite on BrowserStack across multiple browsers and devices (as configured in `browserstack.yml`):

1.  **Ensure Virtual Environment is Active and Dependencies are Installed.**
2.  **Ensure `.env` file is configured with `BROWSERSTACK_USERNAME` and `BROWSERSTACK_ACCESS_KEY`.**
3.  **Execute the following command:**

    ```bash
    "D:\Prayas\MyProjects\El Pais BrowserStack\browserstack_assignment\venv\Scripts\browserstack-sdk.exe" pytest tests/test_el_pais.py
    ```
    **Note:** The path to `browserstack-sdk.exe` must be exact for your environment. If your project path does not contain spaces, you can omit the quotes around the executable path.

    This command uses the `browserstack-sdk` to wrap the `pytest` execution of `tests/test_el_pais.py`, directing the tests to BrowserStack's cloud infrastructure. You can monitor the test progress and results on your BrowserStack Automate dashboard.

## Project Structure

*   `main.py`: The main script that orchestrates the scraping, translation, and analysis.
*   `utils/`: Contains utility modules.
    *   `analyzer.py`: Logic for analyzing repeated words in text.
    *   `scraper.py`: Handles web scraping logic using Selenium.
    *   `translator.py`: Handles text translation using RapidAPI.
*   `tests/`: Contains test files.
    *   `test_el_pais.py`: Pytest test suite for validating the entire flow on BrowserStack.
*   `browserstack.yml`: Configuration file for BrowserStack to define platforms for cross-browser testing.
*   `requirements.txt`: Lists all Python dependencies.
*   `.env.example`: Example file for environment variables.
*   `.env`: Your local environment variables (ignored by Git).
*   `images/`: Directory where scraped article cover images are saved.
*   `log/`: Directory for log files.

## Output Expectations

*   **Local Run:** Console output showing scraped article details, translated titles, download confirmations, and repeated word analysis.
*   **BrowserStack Run:** Test results will be visible on your BrowserStack Automate dashboard, providing logs, screenshots, and video recordings for each platform defined in `browserstack.yml`.

## Troubleshooting

*   **`TimeoutException` during scraping:** This indicates that a web page took too long to load. The script is designed to handle this gracefully by skipping the problematic article and continuing with others.
*   **`browserstack-sdk` not found/command execution issues:** Ensure your virtual environment is active and the command for BrowserStack is precisely entered, including proper quoting for paths with spaces as demonstrated in the "How to Run on BrowserStack" section.
*   **`RAPIDAPI_KEY` or `BROWSERSTACK_` credentials not found:** Double-check your `.env` file to ensure all required environment variables are set correctly.
*   **"No words appeared frequently enough for analysis.":** This is normal if the translated titles of the scraped articles do not contain words repeated three or more times after stopword filtering.
