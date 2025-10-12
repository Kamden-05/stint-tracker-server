from fastapi import FastAPI
from .routes import sessions, stints, laps

app = FastAPI()

app.include_router(stints.router)

@app.get('/')
def root():
    return {"message": "Hello world!"}