import sqlite3
from typing import List
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

DATABASE = "shop.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Returns rows as dictionary-like objects
    return conn


# Initialize table on startup
def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            price REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()


init_db()


# --- Pydantic Models ---
class BookBase(BaseModel):
    title: str
    author: str
    price: float


class BookResponse(BookBase):
    id: int


# --- API Endpoints ---

# 1. POST /books - Add a book (Status 201)
@app.post("/books", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book: BookBase):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO books (title, author, price) VALUES (?, ?, ?)",
        (book.title, book.author, book.price),
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return {"id": new_id, **book.model_dump()}


# 2. GET /books - Fetch all books
@app.get("/books", response_model=List[BookResponse])
def get_all_books():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, author, price FROM books")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


# 3. GET /books/{book_id} - Fetch one book (404 if not found)
@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, author, price FROM books WHERE id = ?", (book_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Book with id {book_id} not found"
        )
    return dict(row)


# 4. PUT /books/{book_id} - Update a book
@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book: BookBase):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE books SET title = ?, author = ?, price = ? WHERE id = ?",
        (book.title, book.author, book.price, book_id),
    )
    conn.commit()
    updated_rows = cursor.rowcount
    conn.close()

    if updated_rows == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Book with id {book_id} not found"
        )
    return {"id": book_id, **book.model_dump()}


# 5. DELETE /books/{book_id} - Delete a book (404 if not found)
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    deleted_rows = cursor.rowcount
    conn.close()

    if deleted_rows == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Book with id {book_id} not found"
        )
    return {"message": f"Book with id {book_id} successfully deleted"}