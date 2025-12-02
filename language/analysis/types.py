from typing import Literal, Optional, Union
from pydantic import BaseModel, Field

PartOfSpeechId = Literal[
    "noun",
    "verb",
    "auxiliary_verb",
    "adjective",
    "adverb",
    "pronoun",
    "determiner",
    "conjunction",
    "preposition",
    "interjection",
    "punctuation",
]

NounGender = Literal["common", "neuter"]
NounDefiniteness = Literal["definite", "indefinite"]
Plurality = Literal["singular", "plural"]

VerbTense = Literal["past tense", "present tense"]
VerbForm = Literal["infinitive", "supine", "imperative"]

PronounForm = Literal["object", "possessive", "subject"]

# Import after Literal types to avoid circular dependencies
from language.analysis.morphology import (  # noqa: E402
    NounMorphology,
    PronounMorphology,
    VerbMorphology,
)
from language.analysis.part_of_speech import PartOfSpeech  # noqa: E402


class BaseToken(BaseModel):
    text: str = Field(description="The original word in the given text.")
    part_of_speech: Optional[PartOfSpeech] = Field(
        description=(
            "The category of the word derived from the universal "
            "part of speech tag."
        )
    )


class NounToken(BaseToken):
    morphology: NounMorphology


class VerbToken(BaseToken):
    morphology: VerbMorphology


class PronounToken(BaseToken):
    morphology: PronounMorphology


Token = Union[NounToken, VerbToken, PronounToken, BaseToken]
