from fastapi import APIRouter
from pydantic import BaseModel, Field

from language.analysis.types import PartOfSpeechId
from language.dictionary.service import Definition

router = APIRouter()


class WordLookup(BaseModel):
    text: str = Field(description="The word to look up")
    pos: PartOfSpeechId | None = Field(
        default=None, description="Optional part of speech for filtering"
    )


class WordDefinition(BaseModel):
    text: str = Field(description="The word that was looked up")
    pos: PartOfSpeechId | None = Field(
        description="Part of speech used for filtering"
    )
    definitions: list[Definition] = Field(
        description="Dictionary definitions filtered by part of speech"
    )


class DefineRequest(BaseModel):
    words: list[WordLookup] = Field(
        min_length=1, description="Words to look up in the dictionary"
    )


class DefineResponse(BaseModel):
    definitions: list[WordDefinition]


@router.post("/define", response_model=DefineResponse)
def define_words(req: DefineRequest) -> DefineResponse:
    # TODO: Implement dictionary lookups
    pass
