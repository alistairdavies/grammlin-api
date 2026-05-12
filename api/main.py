from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import analyse, health
from language.analysis.stanza.analyser import StanzaNLPAnalyser
from language.dictionary.sqlite_store import SqliteDictionaryStore

api = FastAPI()

api.add_middleware(
    CORSMiddleware,  # type: ignore[arg-type]
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# analyser = SpacyNLPAnalyser()
analyser = StanzaNLPAnalyser()
dictionary_store = SqliteDictionaryStore(Path("folkets_sv_en.db"))

api.include_router(health.router)
api.include_router(analyse.router)
