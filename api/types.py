from typing import Literal, Optional, Union
from pydantic import BaseModel, Field

from language.morphology import (
    NounMorphology,
    PronounMorphology,
    VerbMorphology,
)
from language.part_of_speech import PartOfSpeech
from language.lemma import Lemma

NounGender = Literal["common"] | Literal["neuter"]
NounDefiniteness = Literal["definite"] | Literal["indefinite"]
Plurality = Literal["singular"] | Literal["plural"]


class ParseRequest(BaseModel):
    sentence: str


class BaseToken(BaseModel):
    text: str = Field(description="The original word in the given text.")
    lemma: Lemma = Field(
        description="The details for the base form of the word."
    )
    part_of_speech: Optional[PartOfSpeech] = Field(
        description="The category of the word derived from the universal part of speech tag."
    )


class NounToken(BaseToken):
    morphology: NounMorphology


class VerbToken(BaseToken):
    morphology: VerbMorphology


class PronounToken(BaseToken):
    morphology: PronounMorphology


class ParseResponse(BaseModel):
    tokens: list[Union[NounToken, VerbToken, PronounToken, BaseToken]]
