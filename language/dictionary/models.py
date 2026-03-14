from pydantic import BaseModel

from language.analysis.types import PartOfSpeechId


class DictionaryEntry(BaseModel):
    headword: str
    part_of_speech: PartOfSpeechId | None
    translations: list[str]
    definition: str | None
