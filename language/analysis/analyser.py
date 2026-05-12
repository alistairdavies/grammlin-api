from typing import Protocol

from language.analysis.tokens import Token


class NLPAnalyser(Protocol):
    def analyse(self, text: str) -> list[Token]: ...
