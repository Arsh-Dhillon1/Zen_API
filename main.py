from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def check_status():
    return {"message":"Zen Journal API is running"}

