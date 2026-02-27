from typing import Literal

PartOfSpeechId = Literal[
    "noun",
    "numeral",
    "verb",
    "auxiliary_verb",
    "adjective",
    "adverb",
    "pronoun",
    "determiner",
    "conjunction",
    "preposition",
    "interjection",
]

NounGender = Literal["common", "neuter"]
NounDefiniteness = Literal["definite", "indefinite"]
Plurality = Literal["singular", "plural"]

VerbTense = Literal["past tense", "present tense"]
VerbForm = Literal["infinitive", "supine", "imperative"]

PronounForm = Literal["object", "possessive", "subject"]

AdjectiveDegree = Literal["positive", "comparative", "superlative"]
