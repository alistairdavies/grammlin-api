from dataclasses import dataclass
from typing import Literal, Optional


NounGender = Literal["common"] | Literal["neuter"]
NounDefiniteness = Literal["definite"] | Literal["indefinite"]
Plurality = Literal["singular"] | Literal["plural"]

VerbTense = Literal["past tense"] | Literal["present tense"]
VerbForm = Literal["infinitive"] | Literal["supine"] | Literal["imperative"]

PronounForm = Literal["object"] | Literal["possessive"] | Literal["subject"]


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

PRONOUN_FORM_MAP: dict[str, PronounForm] = {
    "Nom": "subject",
    "Acc": "object",
}


@dataclass
class NounMorphology:
    gender: Optional[NounGender]
    definiteness: Optional[NounDefiniteness]
    plurality: Optional[Plurality]

    @classmethod
    def build(cls, morph: dict[str, str]) -> "NounMorphology":
        return cls(
            gender=GENDER_MAP.get(morph.get("Gender", "")),
            plurality=PLURALITY_MAP.get(morph.get("Number", "")),
            definiteness=DEFINITENESS_MAP.get(morph.get("Definite", "")),
        )


@dataclass
class VerbMorphology:
    tense: Optional[VerbTense]
    form: Optional[VerbForm]

    @classmethod
    def build(cls, morph: dict[str, str]) -> "VerbMorphology":
        return cls(
            tense=VERB_TENSE_MAP.get(morph.get("Tense", "")),
            form=VERB_FORM_MAP.get(morph.get("VerbForm", "")),
        )


@dataclass
class PronounMorphology:
    form: PronounForm

    @classmethod
    def build(cls, morph: dict[str, str]) -> "PronounMorphology":
        return cls(
            # Spacy does not return a 'case' for the pronoun when possessive.
            form=PRONOUN_FORM_MAP.get(morph.get("Case", ""), "possessive"),
        )
