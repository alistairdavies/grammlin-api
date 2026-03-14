import json
import sqlite3
from pathlib import Path

from language.analysis.types import PartOfSpeechId
from language.dictionary.models import DictionaryEntry

CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    headword TEXT NOT NULL,
    part_of_speech TEXT,
    translations TEXT NOT NULL,
    definition TEXT
)
"""

CREATE_INDEX = """
CREATE INDEX IF NOT EXISTS idx_headword_pos
ON entries(headword, part_of_speech)
"""

INSERT_ENTRY = """
INSERT INTO entries (headword, part_of_speech, translations, definition)
VALUES (?, ?, ?, ?)
"""

SELECT_BY_HEADWORD = """
SELECT headword, part_of_speech, translations, definition
FROM entries WHERE headword = ?
"""


class SqliteDictionaryStore:
    def __init__(self, db_path: str | Path):
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute(CREATE_TABLE)
        self._conn.execute(CREATE_INDEX)

    def add_entry(self, entry: DictionaryEntry) -> None:
        self._conn.execute(
            INSERT_ENTRY,
            (
                entry.headword,
                entry.part_of_speech,
                json.dumps(entry.translations),
                entry.definition,
            ),
        )
        self._conn.commit()

    def search(
        self, word: str, pos_filter: PartOfSpeechId | None = None
    ) -> list[DictionaryEntry]:
        rows = self._conn.execute(
            SELECT_BY_HEADWORD, (word.lower(),)
        ).fetchall()

        if not rows:
            return []

        all_entries = [self._row_to_entry(row) for row in rows]

        filtered = self._filter_by_pos(all_entries, pos_filter)

        return filtered if filtered else all_entries

    def _filter_by_pos(
        self, entries: list[DictionaryEntry], pos_filter: PartOfSpeechId | None
    ) -> list[DictionaryEntry]:
        if pos_filter is None:
            return entries

        if pos_filter == "auxiliary_verb":
            pos_filter = "verb"

        filtered = [e for e in entries if e.part_of_speech == pos_filter]

        return filtered

    def _row_to_entry(self, row: sqlite3.Row) -> DictionaryEntry:
        return DictionaryEntry(
            headword=row["headword"],
            part_of_speech=row["part_of_speech"],
            translations=json.loads(row["translations"]),
            definition=row["definition"],
        )
