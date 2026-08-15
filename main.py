from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum

app = FastAPI()

journal_entries = []
next_id = 1

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
    content:str
    mood:Mood | None = None

@app.get("/journals/{journal_id}")
def show_entry(journal_id:int):
    for entry in journal_entries:
        if entry["id"] == journal_id:
            return entry

@app.get("/journals")
def show_entries():
    return journal_entries


@app.post("/journals")
def create_journal(journal:JournalCreate):
    global next_id
    
    new_entry = {
    "id": next_id,
    "content": journal.content
    }
    if journal.mood:
        new_entry["mood"] = journal.mood

    journal_entries.append(new_entry)
    next_id+=1
    return new_entry
