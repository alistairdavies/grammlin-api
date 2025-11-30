from typing import Optional, Union
from spacy.tokens import Doc, Token

from language.analysis.morphology import (
    NounMorphology,
    PronounMorphology,
    VerbMorphology,
)
from language.analysis.part_of_speech import map_universal_pos
from api.types import BaseToken, NounToken, PronounToken, VerbToken
from language.dictionary.service import DictionaryService


def parse_token(
    dictionary_service: DictionaryService,
    token: Token,
) -> Optional[Union[NounToken, VerbToken, PronounToken, BaseToken]]:
    pos = map_universal_pos(token.pos_)

    if pos is not None and pos.id == "punctuation":
        return None

    definitions = dictionary_service.search(token.lemma_)
    definition = definitions[0] if len(definitions) != 0 else None

    if pos is not None:
        if pos.id == "noun":
            return NounToken(
                text=token.text,
                part_of_speech=pos,
                morphology=NounMorphology.build(token.morph.to_dict()),
                definition=definition,
            )
        elif pos.id == "pronoun":
            return PronounToken(
                text=token.text,
                part_of_speech=pos,
                morphology=PronounMorphology.build(token.morph.to_dict()),
                definition=definition,
            )
        elif pos.id == "verb" or pos.id == "auxiliary_verb":
            return VerbToken(
                text=token.text,
                part_of_speech=pos,
                morphology=VerbMorphology.build(token.morph.to_dict()),
                definition=definition,
            )

    return BaseToken(
        text=token.text,
        part_of_speech=pos,
        definition=definition,
    )


def parse_tokens(
    dictionary_service: DictionaryService,
    doc: Doc,
) -> list[Union[NounToken, VerbToken, PronounToken, BaseToken]]:
    tokens: list[Union[NounToken, VerbToken, PronounToken, BaseToken]] = []
    for token in doc:
        parsed_token = parse_token(dictionary_service, token)
        if parsed_token is not None:
            tokens.append(parsed_token)
    return tokens
