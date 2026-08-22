from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from database import Base,engine
from enum import Enum

app = FastAPI()

journal_entries = []
next_journal_id = 1
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

class User(BaseModel):
    id:int
    username:str

class JournalCreate(BaseModel):
    content:str
    mood:Mood | None = None

@app.get("/journals/{journal_id}")
def show_entry(journal_id:int):
    for entry in journal_entries:
        if entry["id"] == journal_id:
            return entry
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail="Journal not found"
    )


@app.get("/journals")
def show_entries():
    return journal_entries


@app.post("/journals")
def create_journal(journal:JournalCreate):
    global next_journal_id
    
    new_entry = {
    "id": next_journal_id,
    "content": journal.content
    }
    if journal.mood:
        new_entry["mood"] = journal.mood

    journal_entries.append(new_entry)
    next_journal_id+=1
    return new_entry
