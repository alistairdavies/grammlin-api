from pathlib import Path

from language.dictionary.folkets.parser import parse
from language.dictionary.sqlite_store import SqliteDictionaryStore

XDXF_PATH = Path("folkets_sv_en.xdxf")
DB_PATH = Path("folkets_sv_en.db")


def main() -> None:
    store = SqliteDictionaryStore(DB_PATH)

    total = 0
    compounds = 0
    distinctions = 0

    for entry in parse(XDXF_PATH):
        store.add_entry(entry)
        total += 1
        if entry.distinction:
            distinctions += 1
        if entry.compound_parts:
            compounds += 1

    print("Built dictionary successfully")
    print(f"\t Total Entries: {total}")
    print(f"\t Compounds: {compounds}")
    print(f"\t Distinctions: {distinctions}")


if __name__ == "__main__":
    main()
