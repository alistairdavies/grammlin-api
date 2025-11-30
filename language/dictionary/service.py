import xml.etree.ElementTree as ET
from pathlib import Path

from pydantic import BaseModel


class DictionaryEntry(BaseModel):
    """Represents a dictionary entry."""

    headword: str
    part_of_speech: str | None
    definition: str | None


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

        def_text_elem = def_elem.find("def")
        definition = (
            def_text_elem.text.strip()
            if def_text_elem is not None and def_text_elem.text
            else None
        )

        return DictionaryEntry(
            headword=headword,
            part_of_speech=part_of_speech,
            definition=definition,
        )

    def search(self, word: str) -> list[DictionaryEntry]:
        """Search for a word in the dictionary.

        Args:
            word: The word to search for (case-insensitive)

        Returns:
            List of DictionaryEntry objects if found, empty list otherwise
        """
        if word.lower() in self._entries:
            return self._entries[word.lower()]

        return []
