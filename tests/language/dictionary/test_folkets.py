from pathlib import Path

from language.dictionary.folkets import parse

SINGLE_ENTRY = """<?xml version="1.0" encoding="UTF-8" ?>
<xdxf>
    <lexicon>
        <ar>
            <k>Hund</k>
            <def>
                <gr>nn</gr>
                <dtrn>dog</dtrn>
                <def>a domesticated animal</def>
            </def>
        </ar>
    </lexicon>
</xdxf>"""

MULTIPLE_POS = """<?xml version="1.0" encoding="UTF-8" ?>
<xdxf>
    <lexicon>
        <ar>
            <k>bank</k>
            <def>
                <gr>nn</gr>
                <dtrn>bank</dtrn>
            </def>
        </ar>
        <ar>
            <k>bank</k>
            <def>
                <gr>vb</gr>
                <dtrn>to bank</dtrn>
            </def>
        </ar>
    </lexicon>
</xdxf>"""

NO_POS_TAG = """<?xml version="1.0" encoding="UTF-8" ?>
<xdxf>
    <lexicon>
        <ar>
            <k>word</k>
            <def>
                <dtrn>word</dtrn>
            </def>
        </ar>
    </lexicon>
</xdxf>"""

MULTIPLE_TRANSLATIONS = """<?xml version="1.0" encoding="UTF-8" ?>
<xdxf>
    <lexicon>
        <ar>
            <k>bank</k>
            <def>
                <gr>nn</gr>
                <dtrn>bar</dtrn>
                <dtrn>(sand)bank</dtrn>
            </def>
        </ar>
    </lexicon>
</xdxf>"""


def write_xdxf(tmp_path: Path, content: str) -> Path:
    path = tmp_path / "test.xdxf"
    path.write_text(content, encoding="utf-8")
    return path


class TestFolkets_parse:
    def test_parses_entry(self, tmp_path: Path):
        """
        Given valid XDXF with a single entry
        It returns a DictionaryEntry with parsed fields
        """
        path = write_xdxf(tmp_path, SINGLE_ENTRY)
        entries = list(parse(path))

        assert len(entries) == 1
        assert entries[0].headword == "hund"
        assert entries[0].part_of_speech == "noun"
        assert entries[0].translations == ["dog"]
        assert entries[0].definition == "a domesticated animal"

    def test_resolves_pos_abbreviation(self, tmp_path: Path):
        """
        Given entries with POS abbreviations
        It maps them to first party PartOfSpeechId values
        """
        path = write_xdxf(tmp_path, MULTIPLE_POS)
        entries = list(parse(path))

        assert entries[0].part_of_speech == "noun"
        assert entries[1].part_of_speech == "verb"

    def test_handles_missing_pos(self, tmp_path: Path):
        """
        Given an entry without a POS tag
        It sets part_of_speech to None
        """
        path = write_xdxf(tmp_path, NO_POS_TAG)
        entries = list(parse(path))

        assert entries[0].part_of_speech is None

    def test_parses_multiple_translations(self, tmp_path: Path):
        """
        Given an entry with multiple translation tags
        It returns all translations in a list
        """
        path = write_xdxf(tmp_path, MULTIPLE_TRANSLATIONS)
        entries = list(parse(path))

        assert entries[0].translations == ["bar", "(sand)bank"]
