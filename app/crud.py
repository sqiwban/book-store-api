from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Author, Book
from app.schemas import AuthorCreate, BookCreate, BookUpdate


async def get_author(db: AsyncSession, author_id: int) -> Author | None:
    result = await db.execute(
        select(Author).options(selectinload(Author.books)).where(Author.id == author_id)
    )
    return result.scalar_one_or_none()


async def get_author_by_name(db: AsyncSession, name: str) -> Author | None:
    result = await db.execute(select(Author).where(Author.name == name))
    return result.scalar_one_or_none()


async def get_authors(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[Author]:
    result = await db.execute(select(Author).offset(skip).limit(limit))
    return list(result.scalars().all())


async def create_author(db: AsyncSession, author: AuthorCreate) -> Author:
    db_author = Author(**author.model_dump())
    db.add(db_author)
    await db.flush()
    await db.refresh(db_author)
    return db_author

async def get_book(db: AsyncSession, book_id: int) -> Book | None:
    result = await db.execute(select(Book).where(Book.id == book_id))
    return result.scalar_one_or_none()


async def get_books(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    author_id: int | None = None,
) -> tuple[list[Book], int]:
    query = select(Book)
    count_query = select(func.count(Book.id))

    if author_id:
        query = query.where(Book.author_id == author_id)
        count_query = count_query.where(Book.author_id == author_id)

    total_result = await db.execute(count_query)
    total = total_result.scalar_one()

    result = await db.execute(query.offset(skip).limit(limit))
    return list(result.scalars().all()), total


async def create_book(db: AsyncSession, book: BookCreate) -> Book:
    db_book = Book(**book.model_dump())
    db.add(db_book)
    await db.flush()
    await db.refresh(db_book)
    return db_book


async def update_book(db: AsyncSession, book_id: int, book_update: BookUpdate) -> Book | None:
    db_book = await get_book(db, book_id)
    if not db_book:
        return None

    update_data = book_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_book, field, value)

    await db.flush()
    await db.refresh(db_book)
    return db_book


async def delete_book(db: AsyncSession, book_id: int) -> bool:
    db_book = await get_book(db, book_id)
    if not db_book:
        return False
    await db.delete(db_book)
    await db.flush()
    return True