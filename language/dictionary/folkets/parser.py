from typing import Iterable
import xml.etree.ElementTree as ElementTree
from collections.abc import Iterator
from pathlib import Path
from itertools import chain

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

    articles = lexicon.findall("ar")
    article_entries = list(_parse_articles(articles))
    headwords = {entry.headword for entry in article_entries}
    example_compounds = (
        example_compound
        for example_compound in parse_example_compounds(articles)
        if example_compound.headword not in headwords
    )

    return chain(article_entries, example_compounds)


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
            distinction=parse_distinction(definition),
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


def parse_distinction(definition: ElementTree.Element) -> str | None:
    return definition.attrib.get("cmt", None)


def parse_example_compounds(
    articles: Iterable[ElementTree.Element],
) -> Iterator[DictionaryEntry]:
    for article in articles:
        definition = article.find("def")
        if definition is None:
            continue

        examples = definition.findall("ex")
        for example in examples:
            compound_example = example.find("ex_orig")
            if compound_example is None or not compound_example.text:
                continue

            if "|" not in str(compound_example.text):
                continue

            compound_parts = compound_example.text.strip().lower().split("|")
            headword = "".join(compound_parts)

            translation = example.find("ex_transl")

            yield DictionaryEntry(
                headword=headword,
                part_of_speech=None,
                translations=(
                    [translation.text]
                    if translation is not None and translation.text
                    else []
                ),
                definition=None,
                distinction=None,
                compound_parts=compound_parts,
            )
