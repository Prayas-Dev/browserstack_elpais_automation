import re
from collections import Counter

def find_repeated_words(text, min_count=3, stopwords=None):
    """
    Finds words repeated more than a minimum count in a given text,
    excluding common stopwords. For English text (e.g. translated headers)
    pass stopwords="en"; for Spanish leave as default.
    """
    words = re.findall(r'\b[a-zA-Záéíóúñü]+\b', text.lower())

    if stopwords == "en":
        stopwords = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by", "is", "are", "was", "were", "be", "been", "being"}
    elif stopwords is None:
        stopwords = {"el", "la", "los", "las", "de", "y", "en", "a", "que", "un", "una", "no", "con", "por"}

    words = [word for word in words if word not in stopwords]
    counter = Counter(words)

    return {
        word: count
        for word, count in counter.items()
        if count >= min_count
    }
