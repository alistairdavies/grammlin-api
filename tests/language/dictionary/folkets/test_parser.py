import xml.etree.ElementTree as ElementTree
from pathlib import Path
import pytest

from language.dictionary.folkets.exceptions import (
    ArticleMissingKeyPhrase,
    DictionaryFileNotFound,
    InvalidDictionaryFile,
    InvalidDictionaryFileContent,
    MultipleDefinitionElements,
)
from language.dictionary.folkets.parser import (
    parse,
    parse_definition,
    parse_key_phrase,
    parse_part_of_speech,
    parse_translations,
)
from language.dictionary.models import DictionaryEntry


def create_xdxf(tmp_path: Path, entries: str) -> Path:
    path = tmp_path / "test.xdxf"
    content = (
        '<?xml version="1.0" encoding="UTF-8" ?>'
        "<xdxf><lexicon>"
        f"{entries}"
        "</lexicon></xdxf>"
    )
    path.write_text(content, encoding="utf-8")
    return path


class TestParse:
    def test_file_does_not_exist(self, tmp_path: Path):
        """
        Given a path to a file that does not exist
        It raises an exception
        """
        with pytest.raises(DictionaryFileNotFound):
            list(parse(tmp_path / "invalid.xdxf"))

    def test_invalid_xml(self, tmp_path: Path):
        """
        Given an invalid xml file
        It raises an exception
        """
        xdxf_path = tmp_path / "invalid.xdxf"
        content = "blergh"
        xdxf_path.write_text(content, encoding="utf-8")

        with pytest.raises(InvalidDictionaryFile):
            list(parse(tmp_path / "invalid.xdxf"))

    def test_invalid_xml_dictionary_structure(self, tmp_path: Path):
        """
        Given a path to an xml file that does not contain a lexicon element
        It raises an exception
        """
        xdxf_path = tmp_path / "invalid.xdxf"
        content = '<?xml version="1.0" encoding="UTF-8" ?><xdxf></xdxf>'
        xdxf_path.write_text(content, encoding="utf-8")

        with pytest.raises(InvalidDictionaryFileContent):
            list(parse(xdxf_path))

    def test_parses_xdxf_entries(self, tmp_path: Path):
        """
        Given valid XDXF file of dictionary entries
        It returns a DictionaryEntry for each entry
        """
        entries = """
        <ar>
            <k>Springa</k>
            <def>
                <gr>vb</gr>
                <dtrn>Walk</dtrn>
                <def>Going on a walk</def>
            </def>
        </ar>
        <ar>
            <k>Katt</k>
            <def>
                <gr>nn</gr>
                <dtrn>cat</dtrn>
                <def>a domesticated animal</def>
            </def>
        </ar>
        """
        xdxf = create_xdxf(tmp_path, entries)

        result = list(parse(xdxf))

        assert result == [
            DictionaryEntry(
                headword="springa",
                part_of_speech="verb",
                translations=["Walk"],
                definition="Going on a walk",
                conjunction_parts=None,
            ),
            DictionaryEntry(
                headword="katt",
                part_of_speech="noun",
                translations=["cat"],
                definition="a domesticated animal",
                conjunction_parts=None,
            ),
        ]

    def test_parses_conjunction_entries(self, tmp_path: Path):
        """
        Given valid XDXF file with conjunction entries
        It returns a DictionaryEntry for the conjunction
        """
        entries = """
        <ar>
            <k>skott|kärra</k>
            <def>
                <gr>nn</gr>
            </def>
        </ar>
        """
        xdxf = create_xdxf(tmp_path, entries)

        result = list(parse(xdxf))

        assert result == [
            DictionaryEntry(
                headword="skottkärra",
                part_of_speech="noun",
                translations=[],
                definition=None,
                conjunction_parts=["skott", "kärra"],
            ),
        ]


class TestParseKeyPhrase:
    def test_invalid_article_structure(self):
        """
        Given an article with a missing key phrase
        It raises an exception
        """
        article_element = ElementTree.XML("<ar></ar>")

        with pytest.raises(ArticleMissingKeyPhrase):
            parse_key_phrase(article_element)

    def test_returns_non_compound_key_phrase(self):
        """
        Given an article with a regular key phrase
        It returns the key phrase unmodified with no compound parts
        It returns the key phrase with capitals and whitespace removed
        """
        article_element = ElementTree.XML("<ar><k>food</k></ar>")

        result, compound_parts = parse_key_phrase(article_element)

        assert result == "food"
        assert compound_parts is None

    def test_returns_compound_key_phrase(self):
        """
        Given an article with a key phrase that is a compound
        It returns the combined compounds and its substituent parts
        """
        article_element = ElementTree.XML("<ar><k>barn|skola</k></ar>")

        word, compound_parts = parse_key_phrase(article_element)

        assert word == "barnskola"
        assert compound_parts == ["barn", "skola"]

    def test_sanitises_whitespace(self):
        """
        Given an article with a key phrase
        It returns the key phrase with excess capitals or whitespace removed
        """
        article_element = ElementTree.XML("<ar><k>  FOoD </k></ar>")

        result, _ = parse_key_phrase(article_element)

        assert result == "food"


class TestParseTranslations:
    def test_returns_no_translations(self):
        """
        Given a definition element with no dtrn elements
        It returns an empty list
        """
        def_element = ElementTree.XML("<def></def>")

        result = parse_translations(def_element)

        assert result == []

    def test_returns_direct_translations(self):
        """
        Given a definition element with direct translations
        It returns them as a list
        """
        def_element = ElementTree.XML(
            "<def><dtrn>some direct translation</dtrn></def>"
        )

        result = parse_translations(def_element)

        assert result == ["some direct translation"]

    def test_filters_empty_translations(self):
        """
        Given a direct translation with no content
        It does not return it as a translation
        """
        def_element = ElementTree.XML("<def><dtrn></dtrn></def>")

        result = parse_translations(def_element)

        assert result == []

    def test_filters_whitespace_translations(self):
        """
        Given a direct translation with only whitespace
        It does not return it as a translation
        """
        def_element = ElementTree.XML("<def><dtrn>    </dtrn></def>")

        result = parse_translations(def_element)

        assert result == []


class TestParsePartOfSpeech:
    def test_no_grammar_tag(self):
        """
        Given a definition element with no grammar tag
        It returns None
        """
        def_element = ElementTree.XML("<def></def>")

        result = parse_part_of_speech(def_element)

        assert result is None

    def test_unknown_grmmar_tag(self):
        """
        Given a definition element with an grammar tag with an unknown value
        It returns None
        """
        def_element = ElementTree.XML("<def><gr>foobar</gr></def>")

        result = parse_part_of_speech(def_element)

        assert result is None

    def test_valid_pos_grammar_tag(self):
        """
        Given a definition element with a grammar tag mapped to a POS
        It returns the corresponding POS identifier
        """
        def_element = ElementTree.XML("<def><gr>nn</gr></def>")

        result = parse_part_of_speech(def_element)

        assert result == "noun"


class TestParseDefinition:
    def test_no_inner_definition_tag(self):
        """
        Given a definition element with no inner definition
        It returns None
        """
        def_element = ElementTree.XML("<def></def>")

        result = parse_definition(def_element)

        assert result is None

    def test_multiple_definitions(self):
        """
        Given a definition element with multiple inner definitions
        It raises an error
        """
        def_element = ElementTree.XML("""
            <def>
                <def>First definition</def>
                <def>Another definition</def>
            </def>
        """)

        with pytest.raises(MultipleDefinitionElements):
            parse_definition(def_element)

    def test_empty_definition(self):
        """
        Given a definition element with an empty inner definition
        It returns None
        """
        def_element = ElementTree.XML("<def><def></def></def>")

        result = parse_definition(def_element)

        assert result is None

    def test_valid_definition(self):
        """
        Given a definition element with a valid inner definition
        It returns it unmodified
        """
        def_element = ElementTree.XML(
            "<def><def>some nice definition</def></def>"
        )

        result = parse_definition(def_element)

        assert result == "some nice definition"
