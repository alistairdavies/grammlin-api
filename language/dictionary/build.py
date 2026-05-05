from pathlib import Path

from language.dictionary.folkets.parser import parse
from language.dictionary.sqlite_store import SqliteDictionaryStore

XDXF_PATH = Path("folkets_sv_en.xdxf")
DB_PATH = Path("folkets_sv_en.db")


def main() -> None:
    store = SqliteDictionaryStore(DB_PATH)

    count = 0
    for entry in parse(XDXF_PATH):
        store.add_entry(entry)
        count += 1

    print(f"Built dictionary with {count} entries")


if __name__ == "__main__":
    main()
