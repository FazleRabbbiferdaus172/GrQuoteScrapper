from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import sessionmaker, Session
from typing import List

from ..models.database import engine
from ..models.schemas import AuthorCreate, AuthorUpdate, Author
from ..utils.crud import (get_authors,
                                       get_author_by_id, create_author, update_author, delete_author)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[Author])
def read_authors(offset: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    authors = get_authors(db, offset=offset, limit=limit)
    result = []
    for author in authors:
        result.append(Author(
            id=author.id,
            name=author.name,
        ))
    return authors


@router.get("/{author_id}", response_model=Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    author = get_author_by_id(db, author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@router.post("/", response_model=Author)
def create_new_author(author: AuthorCreate, db: Session = Depends(get_db)):
    db_author = create_author(db, author)
    return db_author


@router.put("/{author_id}", response_model=Author)
def update_existing_author(author_id: int, author: AuthorUpdate, db: Session = Depends(get_db)):
    db_author = update_author(db, author_id, author)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@router.delete("/{author_id}", response_model=Author)
def delete_existing_author(author_id: int, db: Session = Depends(get_db)):
    db_author = delete_author(db, author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author
