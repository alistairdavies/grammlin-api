from typing import Protocol

from language.analysis.types import PartOfSpeechId
from language.dictionary.models import DictionaryEntry


class DictionaryStore(Protocol):
    def add_entry(self, entry: DictionaryEntry) -> None: ...
    def search(
        self, word: str, pos_filter: PartOfSpeechId | None = None
    ) -> list[DictionaryEntry]: ...
