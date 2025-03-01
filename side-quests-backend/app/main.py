from fastapi import FastAPI
from app.db.prisma_connection import lifespan
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
)


@app.get("/")
def root():
    return "Server is running"
