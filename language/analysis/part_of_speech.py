from typing import Optional

from language.analysis.types import PartOfSpeechId


UNIVERSAL_POS_MAP: dict[str, PartOfSpeechId] = {
    "NOUN": "noun",
    "PROPN": "noun",
    "VERB": "verb",
    "AUX": "auxiliary_verb",
    "ADJ": "adjective",
    "ADV": "adverb",
    "PRON": "pronoun",
    "DET": "determiner",
    "CCONJ": "conjunction",
    "SCONJ": "conjunction",
    "ADP": "preposition",
    "INTJ": "interjection",
    "PUNCT": "punctuation",
    "NUM": "numeral",
    "SPACE": "whitespace",
    "SYM": "symbol",
}


def is_punctuation(pos: str) -> bool:
    return pos == "PUNCT"


def map_universal_pos(pos: str) -> Optional[PartOfSpeechId]:
    return UNIVERSAL_POS_MAP.get(pos)
