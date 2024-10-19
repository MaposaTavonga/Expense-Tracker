import sqlite3

# Connect to the database (it will create one if it doesn't exist)
conn = sqlite3.connect('expenses.db')
cur = conn.cursor()

# Create a table for transactions
cur.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    date TEXT NOT NULL,
    type TEXT NOT NULL
)
''')

# Create a table for user budget
cur.execute('''
CREATE TABLE IF NOT EXISTS user_budget (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    budget REAL NOT NULL
)
''')

# Insert an initial budget only if it doesn't already exist
cur.execute("SELECT COUNT(*) FROM user_budget")
if cur.fetchone()[0] == 0:  # Check if the table is empty
    cur.execute("INSERT INTO user_budget (budget) VALUES (1000.00)")  # Set initial budget

conn.commit()
conn.close()
