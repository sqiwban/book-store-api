from fastapi import FastAPI

from app.routers import auth, books, authors, orders

app = FastAPI(
    title="Book Store API",
    description="REST API for managing books, authors and orders",
    version="1.0.0",
)

app.include_router(auth.router)
app.include_router(books.router)
app.include_router(authors.router)
app.include_router(orders.router)

@app.get("/")
async def root():
    return {
        "message": "Book Store API",
        "docs": "/docs",
        "endpoints": {
            "health": "/health",
            "books": "/books",
            "authors": "/authors",
            "auth": "/auth/register, /auth/login",
            "orders": "/orders"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "ok"}