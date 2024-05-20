from sqlalchemy.orm import Session

from ..models.models import Quote, Author
from ..models.schemas import QuoteCreate, QuoteUpdate, AuthorCreate, AuthorUpdate


def get_quotes(db: Session, offset: int = 0, limit: int = 10):
    return db.query(Quote).offset(offset).limit(limit).all()


def get_authors(db: Session, offset: int = 0, limit: int = 10):
    return db.query(Author).offset(offset).limit(limit).all()


def get_quote_by_id(db: Session, quote_id: int):
    return db.query(Quote).filter(Quote.id == quote_id).first()


def create_quote(db: Session, quote: QuoteCreate, author_id: int):
    db_quote = Quote(quote_content=quote.quote_content, author_id=author_id)
    db.add(db_quote)
    db.commit()
    db.refresh(db_quote)
    return db_quote


def update_quote(db: Session, quote_id: int, quote: QuoteUpdate):
    db_quote = get_quote_by_id(db, quote_id)
    if db_quote:
        db_quote.quote_content = quote.quote_content
        if quote.author_name:
            new_author_exists = get_author_by_name(db, name=quote.author_name)
            if not new_author_exists:
                new_author_exists = create_author(db, AuthorCreate(name=quote.author_name))
            db_quote.author_id = new_author_exists.id
        db.commit()
        db.refresh(db_quote)
    return db_quote


def delete_quote(db: Session, quote_id: int):
    db_quote = get_quote_by_id(db, quote_id)
    if db_quote:
        db.delete(db_quote)
        db.commit()
    return db_quote


def get_author_by_id(db: Session, author_id: int):
    return db.query(Author).filter(Author.id == author_id).first()


def create_author(db: Session, author: AuthorCreate):
    db_author = Author(name=author.name)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_author_by_name(db: Session, name: str):
    return db.query(Author).filter(Author.name == name).first()


def update_author(db: Session, author_id: int, author: AuthorUpdate):
    db_author = get_author_by_id(db, author_id)
    if db_author:
        db_author.name = author.name
        db.commit()
        db.refresh(db_author)
    return db_author


def delete_author(db: Session, author_id: int):
    db_author = get_author_by_id(db, author_id)
    if db_author:
        db.delete(db_author)
        db.commit()
    return db_author
