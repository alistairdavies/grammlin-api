import spacy
from spacy.language import Language


def load_swedish_model() -> Language:
    return spacy.load("sv_core_news_lg")
