from fastapi import FastAPI
from app.db.prisma_connection import lifespan
from fastapi.middleware.cors import CORSMiddleware
from app.routes import (
    category_router,
    project_router,
    step_breakdown_router,
    steps_router,
    user_router,
    auth_router,
)

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
)

app.include_router(project_router.router)

app.include_router(category_router.router)

app.include_router(steps_router.router)

app.include_router(step_breakdown_router.router)

app.include_router(user_router.router)

app.include_router(auth_router.router)


@app.get("/", tags=["Root"])
def root():
    return "Server is running"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
