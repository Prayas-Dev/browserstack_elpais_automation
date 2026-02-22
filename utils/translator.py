import logging
import requests
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

def translate_text(text, source="es", target="en"):
    """
    Translate Spanish text to English using RapidAPI Google Translate 113 API.
    Falls back to original text if API fails.
    """

    if not text or not text.strip():
        return text

    url = "https://google-translate113.p.rapidapi.com/api/v1/translator/text"

    payload = {
        "from": source,
        "to": target,
        "text": text
    }

    headers = {
        "Content-Type": "application/json",
        "x-rapidapi-host": "google-translate113.p.rapidapi.com",
        "x-rapidapi-key": RAPIDAPI_KEY
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        # API returns translated text inside "trans"
        return data.get("trans", text)

    except requests.exceptions.RequestException as e:
        logger.warning("RapidAPI translation failed: %s", e)
        return text