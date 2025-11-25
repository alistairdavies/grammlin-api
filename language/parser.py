from typing import Optional, Union
from spacy.tokens import Doc, Token
from uralicNLP import uralicApi

from language.lemma import Lemma
from language.morphology import (
    NounMorphology,
    PronounMorphology,
    VerbMorphology,
)
from language.part_of_speech import is_punctuation, map_universal_pos
from api.types import BaseToken, NounToken, PronounToken, VerbToken


def get_lemma(token: Token) -> Lemma:
    lemm = uralicApi.lemmatize(token.text, "swe", word_boundaries=False)
    lemmat = token.lemma_ if token.lemma_ in lemm else token.text
    return Lemma(text=lemmat)


def parse_token(
    token: Token,
) -> Optional[Union[NounToken, VerbToken, PronounToken, BaseToken]]:
    if is_punctuation(token.pos_):
        return None

    pos = map_universal_pos(token.pos_)
    lemma = get_lemma(token)

    if pos is not None and pos.id == "noun":
        return NounToken(
            text=token.text,
            lemma=lemma,
            part_of_speech=pos,
            morphology=NounMorphology.build(token.morph.to_dict()),
        )
    elif pos is not None and pos.id == "pronoun":
        return PronounToken(
            text=token.text,
            lemma=lemma,
            part_of_speech=pos,
            morphology=PronounMorphology.build(token.morph.to_dict()),
        )
    elif pos is not None and (pos.id == "verb" or pos.id == "auxiliary_verb"):
        return VerbToken(
            text=token.text,
            lemma=lemma,
            part_of_speech=pos,
            morphology=VerbMorphology.build(token.morph.to_dict()),
        )
    else:
        return BaseToken(
            text=token.text,
            lemma=lemma,
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
