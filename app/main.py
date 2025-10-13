from fastapi import FastAPI

from .routes import laps, sessions, stints

app = FastAPI()

app.include_router(sessions.router)
app.include_router(stints.router)
app.include_router(laps.router)


@app.get("/")
def root():
    return {"message": "Hello world!"}
