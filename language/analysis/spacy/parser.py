from typing import Optional
from spacy.tokens import Doc, Token as SpacyToken

from language.analysis.morphology import (
    AdjectiveMorphology,
    NounMorphology,
    PronounMorphology,
    VerbMorphology,
)
from language.analysis.part_of_speech import (
    is_filtered_pos,
    map_universal_pos,
)

from language.analysis.tokens import (
    AdjectiveToken,
    BaseToken,
    NounToken,
    PronounToken,
    Token,
    VerbToken,
)


def parse_token(
    token: SpacyToken,
) -> Optional[Token]:
    if is_filtered_pos(token.pos_):
        return None

    pos = map_universal_pos(token.pos_)

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
) -> list[Token]:
    tokens: list[Token] = []
    for token in doc:
        parsed_token = parse_token(token)
        if parsed_token is not None:
            tokens.append(parsed_token)
    return tokens
