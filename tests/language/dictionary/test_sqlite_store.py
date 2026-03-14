from language.dictionary.sqlite_store import SqliteDictionaryStore
from tests.language.dictionary.factories import DictionaryEntryFactory


class TestSqliteDictionaryStore_search:
    def test_returns_empty(self):
        """
        Given a word that is not in the dictionary
        It returns an empty list
        """
        store = SqliteDictionaryStore(":memory:")
        store.add_entry(DictionaryEntryFactory.create())

        assert store.search("unknown") == []

    def test_returns_matching_entries_given_no_pos_filter(self):
        """
        Given a word and no pos filter
        It returns all entries in the dictionary matching the word
        """
        store = SqliteDictionaryStore(":memory:")
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

    def test_filters_by_pos_when_filter_provided(self):
        """
        Given a word and a pos filter
        It returns the list of matching entries in the dictionary
        """
        store = SqliteDictionaryStore(":memory:")
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

        result = store.search(headword, pos_filter="noun")

        assert len(result) == 1
        assert result[0].part_of_speech == "noun"

    def test_falls_back_to_all_when_no_pos_match(self):
        """
        Given a word and a pos filter
        When the word is in the dictionary but has no pos tag
        It returns the word definition
        """
        store = SqliteDictionaryStore(":memory:")
        entry = DictionaryEntryFactory.create(part_of_speech=None)
        store.add_entry(entry)

        result = store.search(entry.headword, pos_filter="verb")

        assert len(result) == 1

    def test_search_is_case_insensitive(self):
        """
        Given a word to filter by
        It returns dictionary entries case insensitively
        """
        store = SqliteDictionaryStore(":memory:")
        store.add_entry(DictionaryEntryFactory.create(headword="bank"))

        assert len(store.search("Bank")) == 1
        assert len(store.search("BANK")) == 1
