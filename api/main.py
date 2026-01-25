from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import analyse, health
from language.dictionary.service import DictionaryService

api = FastAPI()

api.add_middleware(
    CORSMiddleware,  # type: ignore[arg-type]
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

dictionary_service = DictionaryService(Path("folkets_sv_en.xdxf"))

api.include_router(health.router)
api.include_router(analyse.router)
