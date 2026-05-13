from typing import cast
import stanza
from stanza.models.common.doc import Document

from language.analysis.stanza.parser import parse_tokens
from language.analysis.tokens import (
    Token,
)


class StanzaNLPAnalyser:
    def __init__(self) -> None:
        stanza.download("sv")
        self._model = stanza.Pipeline(
            "sv",
            download_method=stanza.DownloadMethod.NONE,
            verbose=False,
            use_gpu=False,
            processors="tokenize,pos,lemma",
        )

    def analyse(self, text: str) -> list[Token]:
        doc = cast(Document, self._model(text))
        return parse_tokens(doc.sentences)
