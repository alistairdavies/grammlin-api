from typing import Iterable, Optional, cast
import stanza
from stanza.models.common.doc import Sentence, Word, Document

from language.analysis.morphology import (
    AdjectiveMorphology,
    NounMorphology,
    PronounMorphology,
    VerbMorphology,
)
from language.analysis.part_of_speech import is_filtered_pos, map_universal_pos
from language.analysis.tokens import (
    AdjectiveToken,
    BaseToken,
    NounToken,
    PronounToken,
    Token,
    VerbToken,
)


class StanzaNLPAnalyser:
    def __init__(self) -> None:
        self._model = stanza.Pipeline(
            "sv", download_method=stanza.DownloadMethod.NONE
        )

    def analyse(self, text: str) -> list[Token]:
        doc = cast(Document, self._model(text))
        return parse_tokens(doc.sentences)


def parse_tokens(
    doc: Iterable[Sentence],
) -> list[Token]:
    tokens: list[Token] = []
    for sentence in doc:
        for word in sentence.words:
            parsed_token = parse_token(word)
            if parsed_token is not None:
                tokens.append(parsed_token)
    return tokens


def parse_token(
    token: Word,
) -> Optional[Token]:

    if token.pos is not None and is_filtered_pos(token.pos):
        return None

    pos = map_universal_pos(token.pos) if token.pos else None

    lemma = token.lemma if token.lemma else token.text
    if pos is not None:
        if pos == "noun":
            return NounToken(
                text=token.text,
                lemma=lemma,
                part_of_speech=pos,
                morphology=NounMorphology(),
            )
        elif pos == "pronoun":
            return PronounToken(
                text=token.text,
                lemma=lemma,
                part_of_speech=pos,
                morphology=PronounMorphology(form="subject"),
            )
        elif pos == "adjective":
            return AdjectiveToken(
                text=token.text,
                lemma=lemma,
                part_of_speech=pos,
                morphology=AdjectiveMorphology(),
            )
        elif pos == "verb" or pos == "auxiliary_verb":
            return VerbToken(
                text=token.text,
                lemma=lemma,
                part_of_speech=pos,
                morphology=VerbMorphology(),
            )

    return BaseToken(
        text=token.text,
        lemma=lemma,
        part_of_speech=pos,
    )
