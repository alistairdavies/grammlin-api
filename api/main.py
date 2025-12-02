from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import analyse, define

api = FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api.include_router(analyse.router)
api.include_router(define.router)
