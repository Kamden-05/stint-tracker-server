from fastapi import FastAPI
from mangum import Mangum

import logging
import sys

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] [%(name)s:%(lineno)d] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)

from app.routes import (
    lap_router,
    session_router,
    stint_router,
    pit_router,
)

app = FastAPI()

app.include_router(session_router.router)
app.include_router(stint_router.router)
app.include_router(pit_router.router)
app.include_router(lap_router.router)


@app.get("/")
def root():
    return {"message": "PDR Sim Racing Solutions Stint Track Server"}


@app.get("/health")
def get_health():
    return {"status: ok"}


handler = Mangum(app, lifespan="off")
