import spacy
from spacy.language import Language

FOLKETS_LEXICON_DOWNLOAD_URL = (
    "https://folkets-lexikon.csc.kth.se/folkets/folkets_sv_en_public.xdxf"
)


def load_swedish_model() -> Language:
    return spacy.load("sv_core_news_lg")
