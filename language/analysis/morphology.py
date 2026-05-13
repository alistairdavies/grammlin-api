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


def _morph_string_to_dict(morph: str) -> dict[str, str]:
    if "=" not in morph:
        return {}

    return dict(field.split("=", 1) for field in morph.split("|"))


class NounMorphology(BaseModel):
    gender: Optional[NounGender] = None
    definiteness: Optional[NounDefiniteness] = None
    plurality: Optional[Plurality] = None

    @classmethod
    def build(cls, morph: str) -> "NounMorphology":
        morph_dict = _morph_string_to_dict(morph)

        return cls(
            gender=GENDER_MAP.get(morph_dict.get("Gender", "")),
            plurality=PLURALITY_MAP.get(morph_dict.get("Number", "")),
            definiteness=DEFINITENESS_MAP.get(morph_dict.get("Definite", "")),
        )


class VerbMorphology(BaseModel):
    tense: Optional[VerbTense] = None
    form: Optional[VerbForm] = None

    @classmethod
    def build(cls, morph: str) -> "VerbMorphology":
        morph_dict = _morph_string_to_dict(morph)

        return cls(
            tense=VERB_TENSE_MAP.get(morph_dict.get("Tense", "")),
            form=VERB_FORM_MAP.get(morph_dict.get("VerbForm", "")),
        )


class AdjectiveMorphology(BaseModel):
    degree: Optional[AdjectiveDegree] = None

    @classmethod
    def build(cls, morph: str) -> "AdjectiveMorphology":
        morph_dict = _morph_string_to_dict(morph)

        return cls(
            degree=ADJECTIVE_DEGREE_MAP.get(morph_dict.get("Degree", "")),
        )


class PronounMorphology(BaseModel):
    form: PronounForm

    @classmethod
    def build(cls, morph: str) -> "PronounMorphology":
        morph_dict = _morph_string_to_dict(morph)

        return cls(
            form=PRONOUN_FORM_MAP.get(
                morph_dict.get("Case", ""), "possessive"
            ),
        )
