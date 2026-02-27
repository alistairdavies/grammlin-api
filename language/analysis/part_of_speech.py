from typing import Optional

from language.analysis.types import PartOfSpeechId


FILTERED_POS: set[str] = {"PUNCT", "SPACE", "SYM"}

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
    "NUM": "numeral",
}


def is_filtered_pos(pos: str) -> bool:
    return pos in FILTERED_POS


def map_universal_pos(pos: str) -> Optional[PartOfSpeechId]:
    return UNIVERSAL_POS_MAP.get(pos)
