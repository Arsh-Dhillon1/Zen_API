from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from database import Base,engine,SessionLocal
from enum import Enum
from sqlalchemy import String, ForeignKey, select
from sqlalchemy.orm import Mapped, mapped_column


app = FastAPI()

# journal_entries = []
# next_journal_id = 1
next_user_id = 1

class Mood(str, Enum):
    HAPPY = "happy"
    CALM = "calm"
    SAD = "sad"
    ANGRY = "angry"
    ANXIOUS = "anxious"
    GRATEFUL = "grateful"
    EXCITED = "excited"
    NEUTRAL = "neutral"

class JournalCreate(BaseModel):
    content: str
    mood: Mood | None = None

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String)

class Journal(Base):
    __tablename__ = "journals"
    id: Mapped[int] = mapped_column(primary_key=True)
    content:Mapped[str] = mapped_column(String)
    mood:Mapped[str] = mapped_column(String)
    user_id:Mapped[int] = mapped_column(ForeignKey("users.id"))


Base.metadata.create_all(bind=engine)

@app.get("/journals/{journal_id}")
def show_entry(journal_id:int):
    for entry in journals:
        if entry["id"] == journal_id:
            return entry
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail="Journal not found"
    )


@app.get("/journals")
def show_entries():
    db = SessionLocal()
    statement = select(Journal)
    journals = db.scalars(statement).all()
    db.close()

    return journals


@app.post("/journals")
def create_journal(journal:JournalCreate):
    db = SessionLocal()
    new_entry = Journal(
        content = journal.content,
        mood = journal.mood.value if journal.mood else None,
        user_id = 1
    )
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    db.close

    # next_journal_id+=1
    return new_entry
