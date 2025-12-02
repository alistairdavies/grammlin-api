import xml.etree.ElementTree as ET
from pathlib import Path

from pydantic import BaseModel

from language.analysis.types import PartOfSpeechId

# Mapping from Folkets Lexikon dictionary POS abbreviations
# to application POS IDs
DICTIONARY_POS_MAP: dict[str, PartOfSpeechId] = {
    "nn": "noun",  # substantiv (noun)
    "vb": "verb",  # verb
    "jj": "adjective",  # adjektiv (adjective)
    "ab": "adverb",  # adverb
    "pn": "pronoun",  # pronomen (pronoun)
    "pp": "preposition",  # preposition
    "kn": "conjunction",  # konjunktion (conjunction)
    "in": "interjection",  # interjektion (interjection)
}


class DictionaryEntry(BaseModel):
    """Internal representation of a dictionary entry with metadata."""

    headword: str
    part_of_speech: str | None
    translations: list[str]
    definition: str | None


class Definition(BaseModel):
    """Public API representation of a definition."""

    translations: list[str]
    definition: str | None = None


class DictionaryService:
    """Service for loading and searching the XDXF dictionary."""

    def __init__(self, xdxf_path: str | Path):
        """Initialize the dictionary service with the path to the XDXF file.

        Args:
            xdxf_path: Path to the XDXF dictionary file
        """
        self.xdxf_path = Path(xdxf_path)
        self._entries: dict[str, list[DictionaryEntry]] = {}
        self.load()

    def load(self) -> None:
        """Load the dictionary into memory from the XDXF file."""
        tree = ET.parse(self.xdxf_path)
        root = tree.getroot()

        lexicon = root.find("lexicon")
        if lexicon is None:
            raise ValueError("No lexicon element found in XDXF file")

        for ar in lexicon.findall("ar"):
            entries = self._parse_article(ar)
            if entries:
                headword = entries[0].headword
                if headword in self._entries:
                    self._entries[headword].extend(entries)
                else:
                    self._entries[headword] = entries

    def _parse_article(self, ar: ET.Element) -> list[DictionaryEntry]:
        """Parse an article element into DictionaryEntry objects.

        Args:
            ar: The article XML element

        Returns:
            List of DictionaryEntry objects (one per definition)
        """
        k = ar.find("k")
        if k is None or not k.text:
            return []

        headword = k.text.strip()
        entries = []

        for def_elem in ar.findall("def"):
            entry = self._parse_definition(headword, def_elem)
            if entry:
                entries.append(entry)

        return entries

    def _parse_definition(
        self, headword: str, def_elem: ET.Element
    ) -> DictionaryEntry | None:
        """Parse a definition element into a DictionaryEntry.

        Args:
            headword: The headword for this entry
            def_elem: The definition XML element

        Returns:
            DictionaryEntry or None if parsing fails
        """
        gr = def_elem.find("gr")
        part_of_speech = (
            gr.text.strip() if gr is not None and gr.text else None
        )

        # Extract all translations from <dtrn> tags
        translations = [
            dtrn.text.strip() for dtrn in def_elem.findall("dtrn") if dtrn.text
        ]

        # Extract Swedish definition from nested <def> tag
        def_text_elem = def_elem.find("def")
        definition = (
            def_text_elem.text.strip()
            if def_text_elem is not None and def_text_elem.text
            else None
        )

        return DictionaryEntry(
            headword=headword,
            part_of_speech=part_of_speech,
            translations=translations,
            definition=definition,
        )

    def search(
        self, word: str, pos_filter: str | None = None
    ) -> list[DictionaryEntry]:
        """Search for a word in the dictionary with optional POS filtering.

        Args:
            word: The word to search for (case-insensitive)
            pos_filter: Optional application POS ID to filter results.
                       If provided, only returns definitions matching
                       this POS. If no matches found or pos_filter is
                       None, returns all definitions.

        Returns:
            List of DictionaryEntry objects if found, empty list otherwise
        """
        if word.lower() not in self._entries:
            return []

        all_entries = self._entries[word.lower()]

        # If no POS filter provided, return all entries
        if pos_filter is None:
            return all_entries

        # Filter entries by POS
        filtered_entries = [
            entry
            for entry in all_entries
            if entry.part_of_speech is not None
            and DICTIONARY_POS_MAP.get(entry.part_of_speech) == pos_filter
        ]

        # If no matches found with filter, return all entries as fallback
        # This handles cases where dictionary has no POS tags or unknown POS
        if not filtered_entries:
            return all_entries

        return filtered_entries
