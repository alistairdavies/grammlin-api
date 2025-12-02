from pathlib import Path
from tempfile import NamedTemporaryFile

from language.dictionary.service import DictionaryService


def create_test_dictionary(content: str) -> Path:
    """Create a temporary XDXF dictionary file for testing."""
    temp_file = NamedTemporaryFile(
        mode="w", suffix=".xdxf", delete=False, encoding="utf-8"
    )
    temp_file.write(content)
    temp_file.close()
    return Path(temp_file.name)


class TestDictionaryService_search:
    def test_returns_all_definitions_when_no_pos_filter(self):
        """
        Given a word with multiple definitions
        When searching without POS filter
        Then returns all definitions
        """
        xdxf_content = """<?xml version="1.0" encoding="UTF-8" ?>
        <xdxf>
            <lexicon>
                <ar>
                    <k>bank</k>
                    <def>
                        <gr>nn</gr>
                        <dtrn>bar</dtrn>
                        <def>financial institution</def>
                    </def>
                </ar>
                <ar>
                    <k>bank</k>
                    <def>
                        <gr>nn</gr>
                        <dtrn>riverbank</dtrn>
                        <def>riverbank</def>
                    </def>
                </ar>
                <ar>
                    <k>bank</k>
                    <def>
                        <gr>vb</gr>
                        <dtrn>to bank</dtrn>
                        <def>to bank (a plane)</def>
                    </def>
                </ar>
            </lexicon>
        </xdxf>"""

        dict_path = create_test_dictionary(xdxf_content)
        service = DictionaryService(dict_path)

        result = service.search("bank")

        assert len(result) == 3
        assert all(entry.headword == "bank" for entry in result)
        dict_path.unlink()

    def test_filters_by_pos_when_filter_provided(self):
        """
        Given a word with multiple definitions across different POS
        When searching with POS filter
        Then returns only definitions matching that POS
        """
        xdxf_content = """<?xml version="1.0" encoding="UTF-8" ?>
        <xdxf>
            <lexicon>
                <ar>
                    <k>bank</k>
                    <def>
                        <gr>nn</gr>
                        <dtrn>bar</dtrn>
                        <def>financial institution</def>
                    </def>
                </ar>
                <ar>
                    <k>bank</k>
                    <def>
                        <gr>nn</gr>
                        <dtrn>riverbank</dtrn>
                        <def>riverbank</def>
                    </def>
                </ar>
                <ar>
                    <k>bank</k>
                    <def>
                        <gr>vb</gr>
                        <dtrn>to bank</dtrn>
                        <def>to bank (a plane)</def>
                    </def>
                </ar>
            </lexicon>
        </xdxf>"""

        dict_path = create_test_dictionary(xdxf_content)
        service = DictionaryService(dict_path)

        result = service.search("bank", pos_filter="noun")

        assert len(result) == 2
        assert all(entry.part_of_speech == "nn" for entry in result)
        assert result[0].definition == "financial institution"
        assert result[1].definition == "riverbank"
        assert result[0].translations == ["bar"]
        assert result[1].translations == ["riverbank"]
        dict_path.unlink()

    def test_returns_all_definitions_when_no_pos_match(self):
        """
        Given a word with definitions that don't match the filter
        When searching with POS filter
        Then returns all definitions as fallback
        """
        xdxf_content = """<?xml version="1.0" encoding="UTF-8" ?>
        <xdxf>
            <lexicon>
                <ar>
                    <k>word</k>
                    <def>
                        <gr>nn</gr>
                        <dtrn>word</dtrn>
                        <def>a word</def>
                    </def>
                </ar>
            </lexicon>
        </xdxf>"""

        dict_path = create_test_dictionary(xdxf_content)
        service = DictionaryService(dict_path)

        # Search for verb but only noun exists
        result = service.search("word", pos_filter="verb")

        assert len(result) == 1
        assert result[0].part_of_speech == "nn"
        dict_path.unlink()

    def test_returns_all_when_dictionary_has_no_pos(self):
        """
        Given a word with definitions lacking POS tags
        When searching with POS filter
        Then returns all definitions as fallback
        """
        xdxf_content = """<?xml version="1.0" encoding="UTF-8" ?>
        <xdxf>
            <lexicon>
                <ar>
                    <k>word</k>
                    <def>
                        <dtrn>word</dtrn>
                        <def>a definition without POS</def>
                    </def>
                </ar>
            </lexicon>
        </xdxf>"""

        dict_path = create_test_dictionary(xdxf_content)
        service = DictionaryService(dict_path)

        result = service.search("word", pos_filter="noun")

        assert len(result) == 1
        assert result[0].part_of_speech is None
        dict_path.unlink()

    def test_returns_empty_list_for_unknown_word(self):
        """
        Given a word not in dictionary
        When searching
        Then returns empty list
        """
        xdxf_content = """<?xml version="1.0" encoding="UTF-8" ?>
        <xdxf>
            <lexicon>
                <ar>
                    <k>word</k>
                    <def>
                        <gr>nn</gr>
                        <dtrn>word</dtrn>
                        <def>a word</def>
                    </def>
                </ar>
            </lexicon>
        </xdxf>"""

        dict_path = create_test_dictionary(xdxf_content)
        service = DictionaryService(dict_path)

        result = service.search("unknown")

        assert result == []
        dict_path.unlink()

    def test_parses_multiple_translations(self):
        """
        Given a word with multiple translation tags
        When searching
        Then returns all translations in a list
        """
        xdxf_content = """<?xml version="1.0" encoding="UTF-8" ?>
        <xdxf>
            <lexicon>
                <ar>
                    <k>bank</k>
                    <def>
                        <gr>nn</gr>
                        <dtrn>bar</dtrn>
                        <dtrn>(sand)bank</dtrn>
                        <def>sandbank in water</def>
                    </def>
                </ar>
            </lexicon>
        </xdxf>"""

        dict_path = create_test_dictionary(xdxf_content)
        service = DictionaryService(dict_path)

        result = service.search("bank")

        assert len(result) == 1
        assert result[0].translations == ["bar", "(sand)bank"]
        dict_path.unlink()

    def test_handles_entry_with_only_translation(self):
        """
        Given a word with only translation, no Swedish definition
        When searching
        Then returns entry with translation and None definition
        """
        xdxf_content = """<?xml version="1.0" encoding="UTF-8" ?>
        <xdxf>
            <lexicon>
                <ar>
                    <k>kan</k>
                    <def>
                        <dtrn>can</dtrn>
                    </def>
                </ar>
            </lexicon>
        </xdxf>"""

        dict_path = create_test_dictionary(xdxf_content)
        service = DictionaryService(dict_path)

        result = service.search("kan")

        assert len(result) == 1
        assert result[0].translations == ["can"]
        assert result[0].definition is None
        dict_path.unlink()
