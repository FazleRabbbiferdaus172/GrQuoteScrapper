from pydantic import BaseModel
from typing import List, Optional


class QuoteBase(BaseModel):
    quote_content: str
    author_name: str


class QuoteCreate(QuoteBase):
    author_name: str


class QuoteUpdate(QuoteBase):
    pass


class QuoteResponse(QuoteBase):
    id: int

    class Config:
        from_attributes = True


class AuthorBase(BaseModel):
    name: str


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int

    class Config:
        from_attributes = True

# todo: implement tags schema and crud
