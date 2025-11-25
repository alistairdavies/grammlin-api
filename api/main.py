from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.types import ParseResponse, ParseRequest
from language.models import load_swedish_model
from language.parser import parse_tokens

nlp = load_swedish_model()
api = FastAPI()

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
    tokens = parse_tokens(doc)
    return ParseResponse(tokens=tokens)
