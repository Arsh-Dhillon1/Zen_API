from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

journal_entries = []
next_id = 1

class JournalCreate(BaseModel):
    content:str


@app.get("/journals")
def show_entries():
    return journal_entries


@app.post("/journals")
def create_journal(journal:JournalCreate):
    global next_id
    new_entry = {
        "id":next_id,
        "content":journal.content
    }
    journal_entries.append(new_entry)
    next_id+=1
    return new_entry
