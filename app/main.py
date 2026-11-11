from fastapi import FastAPI

app = FastAPI(
    title="Book Store API",
    description="REST API for managing books, authors and orders",
    version="1.0.0",
)


@app.get("/")
async def root():
    return {
        "message": "Book Store API",
        "docs": "/docs",
        "endpoints": {
            "health": "/health",
        }
    }


@app.get("/health")
async def health_check():
    return {"status": "ok"}