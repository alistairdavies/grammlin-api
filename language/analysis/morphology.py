from typing import Optional
from pydantic import BaseModel

from language.analysis.types import (
    AdjectiveDegree,
    NounGender,
    NounDefiniteness,
    Plurality,
    VerbTense,
    VerbForm,
    PronounForm,
)

GENDER_MAP: dict[str, NounGender] = {"Com": "common", "Neut": "neuter"}
DEFINITENESS_MAP: dict[str, NounDefiniteness] = {
    "Def": "definite",
    "Ind": "indefinite",
}
PLURALITY_MAP: dict[str, Plurality] = {
    "Sing": "singular",
    "Plur": "plural",
}

VERB_TENSE_MAP: dict[str, VerbTense] = {
    "Pres": "present tense",
    "Past": "past tense",
}
VERB_FORM_MAP: dict[str, VerbForm] = {
    "Inf": "infinitive",
    "Imp": "imperative",
    "Sup": "supine",
}

ADJECTIVE_DEGREE_MAP: dict[str, AdjectiveDegree] = {
    "Pos": "positive",
    "Cmp": "comparative",
    "Sup": "superlative",
}

PRONOUN_FORM_MAP: dict[str, PronounForm] = {
    "Nom": "subject",
    "Acc": "object",
}


class NounMorphology(BaseModel):
    gender: Optional[NounGender] = None
    definiteness: Optional[NounDefiniteness] = None
    plurality: Optional[Plurality] = None

    @classmethod
    def build(cls, morph: dict[str, str]) -> "NounMorphology":
        return cls(
            gender=GENDER_MAP.get(morph.get("Gender", "")),
            plurality=PLURALITY_MAP.get(morph.get("Number", "")),
            definiteness=DEFINITENESS_MAP.get(morph.get("Definite", "")),
        )


class VerbMorphology(BaseModel):
    tense: Optional[VerbTense] = None
    form: Optional[VerbForm] = None

    @classmethod
    def build(cls, morph: dict[str, str]) -> "VerbMorphology":
        return cls(
            tense=VERB_TENSE_MAP.get(morph.get("Tense", "")),
            form=VERB_FORM_MAP.get(morph.get("VerbForm", "")),
        )


class AdjectiveMorphology(BaseModel):
    degree: Optional[AdjectiveDegree] = None

    @classmethod
    def build(cls, morph: dict[str, str]) -> "AdjectiveMorphology":
        return cls(
            degree=ADJECTIVE_DEGREE_MAP.get(morph.get("Degree", "")),
        )


class PronounMorphology(BaseModel):
    form: PronounForm

    @classmethod
    def build(cls, morph: dict[str, str]) -> "PronounMorphology":
        # Spacy does not return a 'case' for the pronoun when possessive.
        return cls(
            form=PRONOUN_FORM_MAP.get(morph.get("Case", ""), "possessive"),
        )
