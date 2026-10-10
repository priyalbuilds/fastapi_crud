# import sqlite3

# conn = sqlite3.connect("database.db")
# cursor = conn.cursor()

# query = """
#     SELECT name, marks 
#     FROM students 
#     WHERE marks > ? 
#     ORDER BY marks DESC
# """

# cursor.execute(query, (80,))
# rows = cursor.fetchall()

# for name, marks in rows:
#     print(name ,":", marks )

# conn.close()

# import sqlite3

# conn = sqlite3.connect("database.db")
# cursor = conn.cursor()

# insert_query = """
#     INSERT INTO students (name, course, city, marks)
#     VALUES (?, ?, ?, ?)
# """

# cursor.execute(insert_query, ("Vikram", "bca", "udaipur", 67))
# conn.commit() 

# conn.close()