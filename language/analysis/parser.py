from typing import Optional, Union
from spacy.tokens import Doc, Token

from language.analysis.morphology import (
    AdjectiveMorphology,
    NounMorphology,
    PronounMorphology,
    VerbMorphology,
)
from language.analysis.part_of_speech import map_universal_pos
from language.analysis.types import PartOfSpeechId

from language.analysis.tokens import (
    AdjectiveToken,
    BaseToken,
    NounToken,
    PronounToken,
    VerbToken,
)

FILTERED_POS: set[PartOfSpeechId] = {
    "punctuation",
    "whitespace",
    "symbol",
}


def parse_token(
    token: Token,
) -> Optional[
    Union[
        NounToken,
        VerbToken,
        AdjectiveToken,
        PronounToken,
        BaseToken,
    ]
]:
    pos = map_universal_pos(token.pos_)

    if pos in FILTERED_POS:
        return None

    if pos is not None:
        if pos == "noun":
            return NounToken(
                text=token.text,
                lemma=token.lemma_,
                part_of_speech=pos,
                morphology=NounMorphology.build(token.morph.to_dict()),
            )
        elif pos == "pronoun":
            return PronounToken(
                text=token.text,
                lemma=token.lemma_,
                part_of_speech=pos,
                morphology=PronounMorphology.build(token.morph.to_dict()),
            )
        elif pos == "adjective":
            return AdjectiveToken(
                text=token.text,
                lemma=token.lemma_,
                part_of_speech=pos,
                morphology=AdjectiveMorphology.build(token.morph.to_dict()),
            )
        elif pos == "verb" or pos == "auxiliary_verb":
            return VerbToken(
                text=token.text,
                lemma=token.lemma_,
                part_of_speech=pos,
                morphology=VerbMorphology.build(token.morph.to_dict()),
            )

    return BaseToken(
        text=token.text,
        lemma=token.lemma_,
        part_of_speech=pos,
    )


def parse_tokens(
    doc: Doc,
) -> list[
    Union[
        NounToken,
        VerbToken,
        AdjectiveToken,
        PronounToken,
        BaseToken,
    ]
]:
    tokens: list[
        Union[
            NounToken,
            VerbToken,
            AdjectiveToken,
            PronounToken,
            BaseToken,
        ]
    ] = []
    for token in doc:
        parsed_token = parse_token(token)
        if parsed_token is not None:
            tokens.append(parsed_token)
    return tokens
