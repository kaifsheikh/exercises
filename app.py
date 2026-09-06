from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Database Initialize
def init_db():
    conn = sqlite3.connect('workout.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            workout_date TEXT NOT NULL,
            muscle_name TEXT NOT NULL,
            exercise_name TEXT NOT NULL,
            sets INTEGER NOT NULL,
            reps INTEGER NOT NULL,
            weight TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# 1. Main Page
@app.route('/')
def index():
    msg = request.args.get('msg')
    today_input_date = datetime.now().strftime('%Y-%m-%d')
    return render_template('index.html', msg=msg, today_date=today_input_date)

# 2. Form Submit Route (Date ko '07 Sep 2026' format mein save karega)
@app.route('/add', methods=['POST'])
def add_workout():
    raw_date = request.form['workout_date']
    
    # Date ko Month word format ("07 Sep 2026") mein convert karna
    try:
        formatted_date = datetime.strptime(raw_date, '%Y-%m-%d').strftime('%d %b %Y')
    except ValueError:
        formatted_date = raw_date

    muscle = request.form['muscle_name']
    exercise = request.form['exercise_name']
    sets = request.form['sets']
    reps = request.form['reps']
    weight = request.form['weight']

    conn = sqlite3.connect('workout.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO workouts (workout_date, muscle_name, exercise_name, sets, reps, weight)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (formatted_date, muscle, exercise, sets, reps, weight))
    conn.commit()
    conn.close()

    return redirect(url_for('index', msg="Workout Data Successfully Save Ho Gaya!"))

# 3. View Saved Data Route
@app.route('/data')
def view_data():
    conn = sqlite3.connect('workout.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM workouts ORDER BY id DESC')
    records = cursor.fetchall()
    conn.close()
    msg = request.args.get('msg')
    return render_template('data.html', records=records, msg=msg)

# 4. Delete Record Route
@app.route('/delete/<int:id>', methods=['POST'])
def delete_workout(id):
    conn = sqlite3.connect('workout.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM workouts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('view_data', msg="Record Successfully Delete Ho Gaya!"))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)