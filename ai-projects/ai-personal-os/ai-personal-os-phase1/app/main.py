from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import models  # noqa: F401  (registers all tables)
from app.database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs once at startup: create any missing tables.
    Base.metadata.create_all(bind=engine)
    yield    


app = FastAPI(title="AI Personal OS", version="0.1.0", lifespan=lifespan)


@app.get("/health", tags=["System"])            
def health():
    return {"status": "ok"}              
            