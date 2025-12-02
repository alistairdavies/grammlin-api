from pathlib import Path

from fastapi import APIRouter
from pydantic import BaseModel, Field

from language.analysis.types import PartOfSpeechId
from language.dictionary.service import Definition, DictionaryService

dictionary_service = DictionaryService(Path("folkets_sv_en.xdxf"))
router = APIRouter()


class Word(BaseModel):
    text: str = Field(description="The word to look up")
    pos: PartOfSpeechId | None = Field(
        default=None, description="Optional part of speech for filtering"
    )


class DefinitionResult(BaseModel):
    text: str = Field(description="The word that was looked up")
    pos: PartOfSpeechId | None = Field(
        description="Part of speech used for filtering"
    )
    definitions: list[Definition] = Field(
        description="Dictionary definitions filtered by part of speech"
    )


class DefineRequest(BaseModel):
    words: list[Word] = Field(
        min_length=1, description="Words to look up in the dictionary"
    )


class DefineResponse(BaseModel):
    definitions: list[DefinitionResult]


@router.post("/define", response_model=DefineResponse)
def define_words(req: DefineRequest) -> DefineResponse:
    results = []

    for word in req.words:
        entries = dictionary_service.search(word.text, word.pos)

        definitions = [
            Definition(
                translations=entry.translations,
                definition=entry.definition
            )
            for entry in entries
        ]

        results.append(
            DefinitionResult(
                text=word.text,
                pos=word.pos,
                definitions=definitions
            )
        )

    return DefineResponse(definitions=results)
