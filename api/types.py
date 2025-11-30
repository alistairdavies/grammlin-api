from typing import Optional, Union
from pydantic import BaseModel, Field

from language.analysis.morphology import (
    NounMorphology,
    PronounMorphology,
    VerbMorphology,
)
from language.analysis.part_of_speech import PartOfSpeech
from language.dictionary.service import DictionaryEntry


class ParseRequest(BaseModel):
    sentence: str


class BaseToken(BaseModel):
    text: str = Field(description="The original word in the given text.")
    part_of_speech: Optional[PartOfSpeech] = Field(
        description=(
            "The category of the word derived from the universal "
            "part of speech tag."
        )
    )
    definition: Optional[DictionaryEntry] = Field(
        description="The dictionary definition of the word from "
        "folkets lexikon"
    )


class NounToken(BaseToken):
    morphology: NounMorphology


class VerbToken(BaseToken):
    morphology: VerbMorphology


class PronounToken(BaseToken):
    morphology: PronounMorphology


class ParseResponse(BaseModel):
    tokens: list[Union[NounToken, VerbToken, PronounToken, BaseToken]]
