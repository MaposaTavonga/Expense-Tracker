from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Function to connect to the SQLite database
def connect_db():
    return sqlite3.connect('expenses.db')

# Route to set the budget and clear transactions
@app.route('/set_budget', methods=['POST'])
def set_budget():
    budget = request.form['total_budget']

    conn = connect_db()
    cur = conn.cursor()

    # Clear the existing budget and insert the new budget
    cur.execute("DELETE FROM user_budget")  # Clear previous budget
    cur.execute("INSERT INTO user_budget (budget) VALUES (?)", (budget,))

    # Clear all previous transactions
    cur.execute("DELETE FROM transactions")  # Clear all previous transactions

    conn.commit()
    conn.close()

    return redirect('/')

# Home route to display all transactions and the budget
@app.route('/')
def index():
    conn = connect_db()
    cur = conn.cursor()

    # Fetch all transactions
    cur.execute("SELECT * FROM transactions")
    rows = cur.fetchall()

    # Fetch the total budget
    cur.execute("SELECT budget FROM user_budget LIMIT 1")
    budget_row = cur.fetchone()
    total_budget = budget_row[0] if budget_row else 0

    # Calculate remaining balance
    total_expenses = sum(row[2] for row in rows if row[5] == 'expense')  # Adjusted to index 2 for amount
    total_income = sum(row[2] for row in rows if row[5] == 'income')    # Adjusted to index 2 for amount
    remaining_balance = total_budget + total_income - total_expenses

    conn.close()
    return render_template('index.html', transactions=rows, remaining_balance=remaining_balance, total_budget=total_budget)

# Route to add a transaction (income or expense)
@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    description = request.form['description']
    amount = request.form['amount']
    category = request.form['category']
    date = request.form['date']
    transaction_type = request.form['transaction_type']

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO transactions (description, amount, category, date, type) VALUES (?, ?, ?, ?, ?)",
                (description, amount, category, date, transaction_type))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)  # Run the app in debug mode
