
import sqlite3

# 1 ques
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# 2 create books table 
cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT,
        price REAL
    )
""")

cursor.execute("DELETE FROM books")

# 3 insert 3 books in one call using executemany()
books_data = [
    ("Python Basics", "John Doe", 250.0),
    ("Advanced Python", "Jane Smith", 500.0),
    ("Data Science 101", "Alan Turing", 150.0)
]

cursor.executemany("""
    INSERT INTO books (title, author, price)
    VALUES (?, ?, ?)
""", books_data)
conn.commit()

# 4 increase the price of book with id 2 by 10% and print updated rows
cursor.execute("""
    UPDATE books
    SET price = price * 1.10
    WHERE id = 2
""")
conn.commit()
print(f"Rows updated: {cursor.rowcount}")

# 5 delete all books with price less than 300
cursor.execute("DELETE FROM books WHERE price < 300")
conn.commit()

cursor.execute("SELECT id, title, author, price FROM books")
remaining = cursor.fetchall()

print("\nRemaining books:")
for book in remaining:
    print(f"ID: {book[0]}, Title: '{book[1]}', Author: '{book[2]}', Price: {book[3]}")

conn.close()

# final output

# Rows updated: 1
# Remaining books:
# ID: 2, Title: 'Advanced Python', Author: 'Jane Smith', Price: 550.0





