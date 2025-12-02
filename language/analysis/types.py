from typing import Literal

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
