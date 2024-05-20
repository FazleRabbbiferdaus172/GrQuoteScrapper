from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker, Session

from .models.database import engine, create_table
from .api.quotes import router as quotes_router
from .api.authors import router as author_router

create_table(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "healthy"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database connection error")

app.include_router(quotes_router, prefix="/quotes", tags=["quotes"])
app.include_router(author_router, prefix="/authors", tags=["authors"])
