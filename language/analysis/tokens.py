from typing import Optional, Union

from pydantic import BaseModel, Field

from language.analysis.morphology import (
    NounMorphology,
    PronounMorphology,
    VerbMorphology,
)
from language.analysis.part_of_speech import PartOfSpeech
from language.dictionary.service import Definition


class BaseToken(BaseModel):
    text: str = Field(description="The original word in the given text.")
    lemma: str = Field(
        description="The lemma or base form of the original word."
    )
    part_of_speech: Optional[PartOfSpeech] = Field(
        description=(
            "The category of the word derived from the universal "
            "part of speech tag."
        )
    )
    definitions: list[Definition] = Field(
        default_factory=list,
        description="Dictionary definitions for this word",
    )


class NounToken(BaseToken):
    morphology: NounMorphology


class VerbToken(BaseToken):
    morphology: VerbMorphology


class PronounToken(BaseToken):
    morphology: PronounMorphology


Token = Union[NounToken, VerbToken, PronounToken, BaseToken]
