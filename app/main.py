from fastapi import FastAPI
from mangum import Mangum

from .routes import (lap_router, session_router, stint_router,
                     stint_session_router)

app = FastAPI()

app.include_router(session_router.router)
app.include_router(stint_session_router.router)
app.include_router(stint_router.router)
app.include_router(lap_router.router)


@app.get("/")
def root():
    return {"message": "PDR Software Solutions Stint Track Server"}

handler = Mangum(app, lifespan='off')