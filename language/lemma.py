from typing import Optional
from pydantic import BaseModel, computed_field

DICTIONARY_SEARCH_BASE_URL = "https://svenska.se/tre/?sok="


class Lemma(BaseModel):
    text: str

    @computed_field
    @property
    def url(self) -> Optional[str]:
        return f"{DICTIONARY_SEARCH_BASE_URL}{self.text}"
