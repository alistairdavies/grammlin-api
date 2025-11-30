from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.types import ParseResponse, ParseRequest
from language.analysis.models import load_swedish_model
from language.analysis.parser import parse_tokens
from language.dictionary.service import DictionaryService

nlp = load_swedish_model()
api = FastAPI()

dictionary_service = DictionaryService(Path("folkets_sv_en.xdxf"))

api.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@api.post("/parse", response_model=ParseResponse)
def parse_sentence(req: ParseRequest) -> ParseResponse:
    doc = nlp(req.sentence)
    tokens = parse_tokens(dictionary_service, doc)
    return ParseResponse(tokens=tokens)
