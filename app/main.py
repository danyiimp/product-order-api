from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.orders import router as order_router

# from app.core.database import Base, engine
from app.models import *  # noqa: F403, F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Autocreate tables for local dev
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)
    yield
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)


app = FastAPI(
    lifespan=lifespan,
    title="Product Order API",
    version="0.1.0",
    description="A simple product order API with a single endpoint.",
)


app.include_router(order_router, prefix="/orders", tags=["orders"])
