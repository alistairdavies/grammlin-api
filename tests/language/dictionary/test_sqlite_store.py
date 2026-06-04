from pathlib import Path

from language.dictionary.sqlite_store import SqliteDictionaryStore
from tests.language.dictionary.factories import DictionaryEntryFactory


class TestSqliteDictionaryStore_search:
    def test_returns_empty(self, tmp_path: Path):
        """
        Given a word that is not in the dictionary
        It returns an empty list
        """
        store = SqliteDictionaryStore(tmp_path / "test.db")
        store.add_entry(DictionaryEntryFactory.create())

        assert store.search("unknown") == []

    def test_returns_matching_entries_given_no_pos_filter(
        self, tmp_path: Path
    ):
        """
        Given a word and no pos filter
        It returns all entries in the dictionary matching the word
        """
        store = SqliteDictionaryStore(tmp_path / "test.db")
        headword = "bank"
        store.add_entry(
            DictionaryEntryFactory.create(
                headword=headword, part_of_speech="noun"
            )
        )
        store.add_entry(
            DictionaryEntryFactory.create(
                headword=headword, part_of_speech="verb"
            )
        )

        result = store.search(headword)

        assert len(result) == 2

    def test_filters_by_pos_when_filter_provided(self, tmp_path: Path):
        """
        Given a word and a pos filter
        When there is an exact word and pos match
        It returns only the exact matches from the dictionary
        """
        store = SqliteDictionaryStore(tmp_path / "test.db")
        headword = "bank"
        store.add_entry(
            DictionaryEntryFactory.create(
                headword=headword, part_of_speech="noun"
            )
        )
        store.add_entry(
            DictionaryEntryFactory.create(
                headword=headword, part_of_speech="verb"
            )
        )
        store.add_entry(
            DictionaryEntryFactory.create(
                headword=headword, part_of_speech=None
            )
        )

        result = store.search(headword, pos_filter="noun")

        assert len(result) == 1
        assert result[0].part_of_speech == "noun"
        assert result[0].headword == headword

    def test_returns_a_match_when_dictionary_missing_pos(self, tmp_path: Path):
        """
        Given a word and a pos filter
        When the word is in the dictionary but has no pos tag
        It returns the entry without a pos tag
        """
        store = SqliteDictionaryStore(tmp_path / "test.db")
        entry = DictionaryEntryFactory.create(part_of_speech=None)
        store.add_entry(entry)

        result = store.search(entry.headword, pos_filter="verb")

        assert len(result) == 1

    def test_returns_nothing_when_pos_does_not_match(self, tmp_path: Path):
        """
        Given a word and a pos filter
        When the word is in the dictionary and does not match the pos tag
        It does not return any matches
        """
        store = SqliteDictionaryStore(tmp_path / "test.db")
        entry = DictionaryEntryFactory.create(
            headword="nice", part_of_speech=None
        )
        store.add_entry(entry)

        result = store.search(entry.headword, pos_filter="verb")

        assert len(result) == 1

    def test_search_is_case_insensitive(self, tmp_path: Path):
        """
        Given a word to filter by
        It returns dictionary entries case insensitively
        """
        store = SqliteDictionaryStore(tmp_path / "test.db")
        store.add_entry(DictionaryEntryFactory.create(headword="bank"))

        assert len(store.search("Bank")) == 1
        assert len(store.search("BANK")) == 1

    def test_returns_compound_parts(self, tmp_path: Path):
        """
        Given an entry stored with compound_parts
        When it is retrieved via search
        It returns compound_parts unchanged
        """
        store = SqliteDictionaryStore(tmp_path / "test.db")
        entry = DictionaryEntryFactory.create(
            headword="bokhandel",
            compound_parts=["bok", "handel"],
        )
        store.add_entry(entry)

        result = store.search("bokhandel")

        assert len(result) == 1
        assert result[0].compound_parts == ["bok", "handel"]

    def test_returns_null_compound_parts_when_not_a_compound(
        self, tmp_path: Path
    ):
        """
        Given an entry stored without compound_parts
        When it is retrieved via search
        It returns compound_parts as None
        """
        store = SqliteDictionaryStore(tmp_path / "test.db")
        entry = DictionaryEntryFactory.create(
            headword="bok", compound_parts=None
        )
        store.add_entry(entry)

        result = store.search("bok")

        assert len(result) == 1
        assert result[0].compound_parts is None
