from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import sessionmaker, Session
from typing import List

from ..models.database import engine
from ..models.schemas import QuoteResponse, QuoteCreate, QuoteUpdate, AuthorCreate
from ..utils.crud import (get_quotes, get_quote_by_id, create_quote, update_quote, delete_quote,
                                       get_author_by_id, create_author, get_author_by_name)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[QuoteResponse])
def read_quotes(offset: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    quotes = get_quotes(db, offset=offset, limit=limit)
    results = []
    for quote in quotes:
        author = get_author_by_id(db, author_id=quote.author_id)
        results.append(QuoteResponse(
            id=quote.id,
            quote_content=quote.quote_content,
            author_name=author.name if author else "Unknown"))
    return results


@router.get("/{quote_id}", response_model=QuoteResponse)
def read_quote(quote_id: int, db: Session = Depends(get_db)):
    quote = get_quote_by_id(db, quote_id)
    if quote is None:
        raise HTTPException(status_code=404, detail="Quote not found")
    author = get_author_by_id(db, quote.author_id)
    return QuoteResponse(
        id=quote.id,
        quote_content=quote.quote_content,
        author_name=author.name if author else "Unknown")


@router.post("/", response_model=QuoteResponse)
def create_new_quote(quote: QuoteCreate, db: Session = Depends(get_db)):
    author = get_author_by_name(db, quote.author_name)
    if not author:
        author = create_author(db, AuthorCreate(name=quote.author_name))
    db_quote = create_quote(db, quote, author.id)
    return QuoteResponse(
        id=db_quote.id,
        quote_content=db_quote.quote_content,
        author_name=author.name)


@router.put("/{quote_id}", response_model=QuoteResponse)
def update_existing_quote(quote_id: int, quote: QuoteUpdate, db: Session = Depends(get_db)):
    db_quote = update_quote(db, quote_id, quote)
    if db_quote is None:
        raise HTTPException(status_code=404, detail="Quote not found")
    author = get_author_by_id(db, db_quote.author_id)
    return {
        "id": db_quote.id,
        "quote_content": db_quote.quote_content,
        "author_name": author.name if author else "Unknown"
    }


@router.delete("/{quote_id}")
def delete_existing_quote(quote_id: int, db: Session = Depends(get_db)):
    db_quote = delete_quote(db, quote_id)
    if db_quote is None:
        raise HTTPException(status_code=404, detail="Quote not found")
    author = get_author_by_id(db, db_quote.author_id)
    return db_quote
