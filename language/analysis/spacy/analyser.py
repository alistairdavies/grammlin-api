import spacy
from language.analysis.spacy.parser import parse_tokens
from language.analysis.tokens import Token


class SpacyNLPAnalyser:
    def __init__(self) -> None:
        self._model = spacy.load("sv_core_news_lg", exclude=["parser"])

    def analyse(self, text: str) -> list[Token]:
        doc = self._model(text)
        return parse_tokens(doc)
