from typing import Iterable
import xml.etree.ElementTree as ElementTree
from collections.abc import Iterator
from pathlib import Path

from language.analysis.types import PartOfSpeechId
from language.dictionary.folkets.exceptions import (
    ArticleMissingKeyPhrase,
    DictionaryFileNotFound,
    InvalidDictionaryFile,
    InvalidDictionaryFileContent,
    MultipleDefinitionElements,
)
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
    try:
        tree = ElementTree.parse(path)
    except FileNotFoundError:
        raise DictionaryFileNotFound(f"Dictionary XML file '{path}' not found")
    except ElementTree.ParseError:
        raise InvalidDictionaryFile("Unable to parse dictionary XML file")

    root = tree.getroot()

    lexicon = root.find("lexicon")
    if lexicon is None:
        raise InvalidDictionaryFileContent(
            "No lexicon element found in XDXF file"
        )

    return _parse_articles(lexicon.findall("ar"))


def _parse_articles(
    articles: Iterable[ElementTree.Element],
) -> Iterator[DictionaryEntry]:
    for article in articles:
        definition = article.find("def")
        if definition is None:
            continue

        headword, compound_parts = parse_key_phrase(article)

        yield DictionaryEntry(
            headword=headword,
            part_of_speech=parse_part_of_speech(definition),
            translations=parse_translations(definition),
            definition=parse_definition(definition),
            compound_parts=compound_parts,
        )


def parse_key_phrase(
    article: ElementTree.Element,
) -> tuple[str, list[str] | None]:
    key_phrase = article.find("k")
    if key_phrase is None or not key_phrase.text:
        raise ArticleMissingKeyPhrase

    headword = key_phrase.text.strip().lower()

    if "|" in headword:
        compound_parts = headword.split("|")
        return "".join(compound_parts), compound_parts
    else:
        return headword, None


def parse_translations(definition: ElementTree.Element) -> list[str]:
    translations = []

    for dtrn in definition.findall("dtrn"):
        if dtrn.text:
            translation = dtrn.text.strip()
            if translation:
                translations.append(translation)
    return translations


def parse_part_of_speech(
    definition: ElementTree.Element,
) -> PartOfSpeechId | None:
    gr = definition.find("gr")
    if gr is None:
        return None

    if gr.text is None:
        return None

    grammar_tag = gr.text.strip()
    return FOLKETS_POS_MAP.get(grammar_tag)


def parse_definition(
    definition: ElementTree.Element,
) -> str | None:
    def_text_elems = definition.findall("def")

    if len(def_text_elems) > 1:
        raise MultipleDefinitionElements(
            "Expected one definition per dictionary entry but found multiple"
        )

    if len(def_text_elems) == 0:
        return None

    def_text_elem = def_text_elems.pop()
    return def_text_elem.text.strip() if def_text_elem.text else None
