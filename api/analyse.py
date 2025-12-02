from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator

from language.analysis.types import BaseToken, NounToken, PronounToken, VerbToken
from language.detection import is_swedish

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
    if not is_swedish(req.sentence):
        raise HTTPException(
            status_code=422, detail="Input must be Swedish text"
        )

    # TODO: Call parser without dictionary lookups
    pass
