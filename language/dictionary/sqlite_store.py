import json
import sqlite3
import threading
from pathlib import Path

from language.analysis.types import PartOfSpeechId
from language.dictionary.models import DictionaryEntry

CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    headword TEXT NOT NULL,
    distinction TEXT,
    part_of_speech TEXT,
    translations TEXT NOT NULL,
    definition TEXT,
    compound_parts TEXT
)
"""

CREATE_INDEX = """
CREATE INDEX IF NOT EXISTS idx_headword_pos
ON entries(headword, part_of_speech)
"""

INSERT_ENTRY = """
INSERT INTO entries
(headword, part_of_speech, translations,
definition, compound_parts, distinction)
VALUES (?, ?, ?, ?, ?, ?)
"""

SELECT_BY_HEADWORD = """
SELECT headword, part_of_speech, translations, definition, distinction,
compound_parts
FROM entries WHERE headword = ?
"""


class SqliteDictionaryStore:
    def __init__(self, db_path: str | Path):
        self._db_path = str(db_path)
        self._local = threading.local()
        self._ensure_schema()

    def _connection(self) -> sqlite3.Connection:
        if not hasattr(self._local, "conn"):
            conn = sqlite3.connect(self._db_path)
            conn.row_factory = sqlite3.Row
            self._local.conn = conn
        return self._local.conn

    def _ensure_schema(self) -> None:
        conn = self._connection()
        conn.execute(CREATE_TABLE)
        conn.execute(CREATE_INDEX)
        conn.commit()

    def add_entry(self, entry: DictionaryEntry) -> None:
        conn = self._connection()
        conn.execute(
            INSERT_ENTRY,
            (
                entry.headword,
                entry.part_of_speech,
                json.dumps(entry.translations),
                entry.definition,
                json.dumps(entry.compound_parts),
                entry.distinction,
            ),
        )
        conn.commit()

    def search(
        self, word: str, pos_filter: PartOfSpeechId | None = None
    ) -> list[DictionaryEntry]:
        conn = self._connection()
        rows = conn.execute(SELECT_BY_HEADWORD, (word.lower(),)).fetchall()

        if not rows:
            return []

        all_entries = [self._row_to_entry(row) for row in rows]
        filtered = self._filter_by_pos(all_entries, pos_filter)

        if len(filtered) > 0:
            return filtered

        return self._filter_by_empty_pos(all_entries)

    def _filter_by_pos(
        self, entries: list[DictionaryEntry], pos_filter: PartOfSpeechId | None
    ) -> list[DictionaryEntry]:
        if pos_filter is None:
            return entries

        if pos_filter == "auxiliary_verb":
            pos_filter = "verb"

        filtered = [e for e in entries if e.part_of_speech == pos_filter]

        return filtered

    def _filter_by_empty_pos(
        self, entries: list[DictionaryEntry]
    ) -> list[DictionaryEntry]:
        filtered = [e for e in entries if e.part_of_speech is None]

        return filtered

    def _row_to_entry(self, row: sqlite3.Row) -> DictionaryEntry:
        raw_parts = row["compound_parts"]
        return DictionaryEntry(
            headword=row["headword"],
            part_of_speech=row["part_of_speech"],
            translations=json.loads(row["translations"]),
            definition=row["definition"],
            compound_parts=json.loads(raw_parts) if raw_parts else None,
            distinction=row["distinction"],
        )
