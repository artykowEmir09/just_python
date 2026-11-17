from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import models  # noqa: F401  (registers all tables)
from app.database import Base, engine
from app.routers import notes, tags, tasks


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs once at startup: create any missing tables.
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="AI Personal OS", version="0.2.0", lifespan=lifespan)

API_PREFIX = "/api/v1"
app.include_router(notes.router, prefix=API_PREFIX)
app.include_router(tasks.router, prefix=API_PREFIX)
app.include_router(tags.router, prefix=API_PREFIX)


@app.get("/health", tags=["System"])
def health():
    return {"status": "ok"}
