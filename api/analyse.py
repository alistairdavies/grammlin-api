from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator

from language.analysis.models import load_swedish_model
from language.analysis.parser import parse_tokens
from language.analysis.tokens import (
    BaseToken,
    NounToken,
    PronounToken,
    VerbToken,
)
from language.detection import is_swedish
from language.dictionary.service import Definition

nlp = load_swedish_model()
router = APIRouter()


class AnalyseRequest(BaseModel):
    sentence: str = Field(
        min_length=1, max_length=1000, description="Swedish text to analyse"
    )

    @field_validator("sentence")
    @classmethod
    def strip_and_validate_whitespace(cls, v: str) -> str:
        stripped = v.strip()
        if not stripped:
            raise ValueError("Sentence cannot be whitespace only")
        return stripped


class AnalyseResponse(BaseModel):
    tokens: list[NounToken | VerbToken | PronounToken | BaseToken]


@router.post("/analyse", response_model=AnalyseResponse)
def analyse_sentence(req: AnalyseRequest) -> AnalyseResponse:
    from api.main import dictionary_service

    if not is_swedish(req.sentence):
        raise HTTPException(
            status_code=422, detail="Input must be Swedish text"
        )

    doc = nlp(req.sentence)
    tokens = parse_tokens(doc)

    for token in tokens:
        pos_filter = token.part_of_speech.id if token.part_of_speech else None
        entries = dictionary_service.search(token.lemma.lower(), pos_filter)
        token.definitions = [
            Definition(
                translations=entry.translations, definition=entry.definition
            )
            for entry in entries
        ]

    return AnalyseResponse(tokens=tokens)
