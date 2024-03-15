from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database initialization
conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users 
             (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, age INTEGER, dob DATE)''')
conn.commit()
conn.close()

# Index route
@app.route('/')
def index():
    return render_template('index.html')

# Add user route
@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form['name']
    email = request.form['email']
    age = request.form['age']
    dob = request.form['dob']

    # Validate age
    try:
        age = int(age)
        if age <= 0:
            raise ValueError
    except ValueError:
        flash('Age must be a positive integer.')
        return redirect(url_for('index'))

    # Validate email
    if '@' not in email:
        flash('Invalid email format.')
        return redirect(url_for('index'))

    # Add user to the database
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (name, email, age, dob) VALUES (?, ?, ?, ?)", (name, email, age, dob))
    conn.commit()
    conn.close()
    
    flash('User added successfully.')
    return redirect(url_for('index'))

# Retrieve users route
@app.route('/users')
def users():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    conn.close()
    print(users)  # Debugging statement
    return render_template('user.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)
