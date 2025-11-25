from fastapi import FastAPI
import spacy

from api.types import (
    BaseToken,
    NounToken,
    ParseResponse,
    ParseRequest,
    VerbToken,
    PronounToken,
)

from fastapi.middleware.cors import CORSMiddleware
from language.lemma import Lemma
from language.morphology import (
    NounMorphology,
    PronounMorphology,
    VerbMorphology,
)
from language.part_of_speech import is_punctuation, map_universal_pos
from uralicNLP import uralicApi

nlp = spacy.load("sv_core_news_lg")
api = FastAPI()


api.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@api.post("/parse", response_model=ParseResponse)
def parse_sentence(req: ParseRequest):
    doc = nlp(req.sentence)
    tokens = []
    for token in doc:
        if is_punctuation(token.pos_):
            continue

        pos = map_universal_pos(token.pos_)
        lemm = uralicApi.lemmatize(token.text, "swe", word_boundaries=False)
        lemmat = token.lemma_ if token.lemma_ in lemm else token.text
        lemma = Lemma(text=lemmat)
        if pos is not None and pos.id == "noun":
            tokens.append(
                NounToken(
                    text=token.text,
                    lemma=lemma,
                    part_of_speech=pos,
                    morphology=NounMorphology.build(token.morph.to_dict()),
                )
            )
        elif pos is not None and pos.id == "pronoun":
            tokens.append(
                PronounToken(
                    text=token.text,
                    lemma=lemma,
                    part_of_speech=pos,
                    morphology=PronounMorphology.build(token.morph.to_dict()),
                )
            )
        elif pos is not None and (
            pos.id == "verb" or pos.id == "auxiliary_verb"
        ):
            tokens.append(
                VerbToken(
                    text=token.text,
                    lemma=lemma,
                    part_of_speech=pos,
                    morphology=VerbMorphology.build(token.morph.to_dict()),
                )
            )

        else:
            tokens.append(
                BaseToken(
                    text=token.text,
                    lemma=lemma,
                    part_of_speech=pos,
                )
            )

    return ParseResponse(tokens=tokens)
