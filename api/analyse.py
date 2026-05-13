from fastapi import APIRouter
from pydantic import BaseModel, Field, field_validator

from language.analysis.tokens import (
    AdjectiveToken,
    BaseToken,
    NounToken,
    PronounToken,
    VerbToken,
)
from language.detection import is_swedish
from language.analysis.tokens import Definition

router = APIRouter()


class AnalyseRequest(BaseModel):
    sentence: str = Field(
        min_length=1, max_length=1000, description="Swedish text to analyse"
    )

    @field_validator("sentence")
    @classmethod
    def validate_sentence(cls, v: str) -> str:
        stripped = v.strip()
        if not stripped:
            raise ValueError("Sentence cannot be whitespace only")

        if not is_swedish(v):
            raise ValueError("Input must be Swedish text")

        return stripped


class AnalyseResponse(BaseModel):
    tokens: list[
        NounToken | VerbToken | AdjectiveToken | PronounToken | BaseToken
    ]


@router.post("/analyse", response_model=AnalyseResponse)
def analyse_sentence(req: AnalyseRequest) -> AnalyseResponse:
    from api.main import dictionary_store, analyser

    tokens = analyser.analyse(req.sentence)

    for token in tokens:
        pos_filter = token.part_of_speech
        entries = dictionary_store.search(token.lemma, pos_filter)
        if len(entries) == 0:
            entries = dictionary_store.search(token.text, pos_filter)

        token.definitions = [
            Definition(
                translations=entry.translations, definition=entry.definition
            )
            for entry in entries
        ]

    return AnalyseResponse(tokens=tokens)
