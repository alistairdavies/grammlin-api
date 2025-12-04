from typing import Optional, Union
from spacy.tokens import Doc, Token

from language.analysis.morphology import (
    NounMorphology,
    PronounMorphology,
    VerbMorphology,
)
from language.analysis.part_of_speech import map_universal_pos
from language.analysis.tokens import (
    BaseToken,
    NounToken,
    PronounToken,
    VerbToken,
)


def parse_token(
    token: Token,
) -> Optional[Union[NounToken, VerbToken, PronounToken, BaseToken]]:
    pos = map_universal_pos(token.pos_)

    if pos is not None and pos.id == "punctuation":
        return None

    if pos is not None:
        if pos.id == "noun":
            return NounToken(
                text=token.text,
                lemma=token.lemma_,
                part_of_speech=pos,
                morphology=NounMorphology.build(token.morph.to_dict()),
            )
        elif pos.id == "pronoun":
            return PronounToken(
                text=token.text,
                lemma=token.lemma_,
                part_of_speech=pos,
                morphology=PronounMorphology.build(token.morph.to_dict()),
            )
        elif pos.id == "verb" or pos.id == "auxiliary_verb":
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
) -> list[Union[NounToken, VerbToken, PronounToken, BaseToken]]:
    tokens: list[Union[NounToken, VerbToken, PronounToken, BaseToken]] = []
    for token in doc:
        parsed_token = parse_token(token)
        if parsed_token is not None:
            tokens.append(parsed_token)
    return tokens
