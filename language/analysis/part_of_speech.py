from typing import Optional
from pydantic import BaseModel

from language.analysis.types import PartOfSpeechId


class PartOfSpeech(BaseModel):
    title: str
    id: PartOfSpeechId


UNIVERSAL_POS_MAP = {
    "NOUN": PartOfSpeech(id="noun", title="Noun"),
    "PROPN": PartOfSpeech(id="noun", title="Noun"),
    "VERB": PartOfSpeech(id="verb", title="Verb"),
    "AUX": PartOfSpeech(id="auxiliary_verb", title="Auxiliary verb"),
    "ADJ": PartOfSpeech(id="adjective", title="Adjective"),
    "ADV": PartOfSpeech(id="adverb", title="Adverb"),
    "PRON": PartOfSpeech(id="pronoun", title="Pronoun"),
    "DET": PartOfSpeech(id="determiner", title="Determiner"),
    "CCONJ": PartOfSpeech(id="conjunction", title="Conjunction"),
    "SCONJ": PartOfSpeech(id="conjunction", title="Conjunction"),
    "ADP": PartOfSpeech(id="preposition", title="Preposition"),
    "INTJ": PartOfSpeech(id="interjection", title="Interjection"),
    "PUNCT": PartOfSpeech(id="punctuation", title="Punctuation"),
    "NUM": PartOfSpeech(id="numeral", title="Numeral"),
}


def is_punctuation(pos: str) -> bool:
    return pos == "PUNCT"


def map_universal_pos(pos: str) -> Optional[PartOfSpeech]:
    return UNIVERSAL_POS_MAP.get(pos)
