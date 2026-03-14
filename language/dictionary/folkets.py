import xml.etree.ElementTree as ET
from collections.abc import Iterator
from pathlib import Path

from language.analysis.types import PartOfSpeechId
from language.dictionary.models import DictionaryEntry

FOLKETS_POS_MAP: dict[str, PartOfSpeechId] = {
    "nn": "noun",
    "vb": "verb",
    "jj": "adjective",
    "ab": "adverb",
    "pn": "pronoun",
    "pp": "preposition",
    "kn": "conjunction",
    "in": "interjection",
    "rg": "numeral",
    "article": "determiner",
}


def parse(path: Path) -> Iterator[DictionaryEntry]:
    tree = ET.parse(path)
    root = tree.getroot()

    lexicon = root.find("lexicon")
    if lexicon is None:
        raise ValueError("No lexicon element found in XDXF file")

    for ar in lexicon.findall("ar"):
        k = ar.find("k")
        if k is None or not k.text:
            continue

        headword = k.text.strip().lower()

        for def_elem in ar.findall("def"):
            entry = _parse_definition(headword, def_elem)
            if entry:
                yield entry


def _parse_definition(
    headword: str, def_elem: ET.Element
) -> DictionaryEntry | None:
    gr = def_elem.find("gr")
    raw_pos = gr.text.strip() if gr is not None and gr.text else None
    part_of_speech = FOLKETS_POS_MAP.get(raw_pos) if raw_pos else None

    translations = [
        dtrn.text.strip() for dtrn in def_elem.findall("dtrn") if dtrn.text
    ]

    def_text_elem = def_elem.find("def")
    definition = (
        def_text_elem.text.strip()
        if def_text_elem is not None and def_text_elem.text
        else None
    )

    return DictionaryEntry(
        headword=headword,
        part_of_speech=part_of_speech,
        translations=translations,
        definition=definition,
    )
