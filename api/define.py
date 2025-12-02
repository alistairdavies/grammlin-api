from fastapi import APIRouter
from pydantic import BaseModel, Field

from language.analysis.types import PartOfSpeechId
from language.dictionary.service import Definition

router = APIRouter()


class DefineRequest(BaseModel):
    text: str = Field(description="The word to look up")
    pos: PartOfSpeechId | None = Field(
        default=None, description="Optional part of speech for filtering"
    )


class DefineResponse(BaseModel):
    text: str = Field(description="The word that was looked up")
    pos: PartOfSpeechId | None = Field(
        description="Part of speech used for filtering"
    )
    definitions: list[Definition] = Field(
        description="Dictionary definitions filtered by part of speech"
    )


@router.post("/define", response_model=DefineResponse)
def define_word(req: DefineRequest) -> DefineResponse:
    from api.main import dictionary_service

    entries = dictionary_service.search(req.text, req.pos)

    definitions = [
        Definition(
            translations=entry.translations,
            definition=entry.definition
        )
        for entry in entries
    ]

    return DefineResponse(
        text=req.text,
        pos=req.pos,
        definitions=definitions
    )
