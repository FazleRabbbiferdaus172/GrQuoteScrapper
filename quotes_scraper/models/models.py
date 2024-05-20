from sqlalchemy import Table, Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .database import Base

quote_tag = Table('quote_tag', Base.metadata,
                  Column('quote_id', Integer, ForeignKey('quote.id'), primary_key=True),
                  Column('tag_id', Integer, ForeignKey('tag.id'), primary_key=True)
                  )


class Quote(Base):
    __tablename__ = "quote"

    id = Column(Integer, primary_key=True)
    quote_content = Column('quote_content', Text(), nullable=False)
    author_id = Column(Integer, ForeignKey('author.id'))
    tags = relationship('Tag', secondary=quote_tag, back_populates="quotes")


class Author(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True)
    name = Column('name', String(50), unique=True, nullable=False)
    quotes = relationship('Quote', backref='author', lazy=True)


class Tag(Base):
    __tablename__ = "tag"

    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True, nullable=False)
    quotes = relationship('Quote', secondary=quote_tag, back_populates="tags")
