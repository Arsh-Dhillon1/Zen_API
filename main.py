from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()

class Journal(BaseModel):
    content:str

@app.get("/")
def check_status():
    return {"message":"Zen Journal API is running"}

@app.post("/journals")
def journals(journal:Journal):
    return {f"Content Successfully sent to the server! {journal.content}"}
    