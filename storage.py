import sqlite3
from workout import Workout

# When program is run the database is created or reinitialized
def initialize_db():
    with sqlite3.connect('workout_storage.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS workouts (
            exercise TEXT,
            sets INTEGER,
            reps INTEGER,
            weight REAL,
            date TEXT
        )
        ''')
        conn.commit()

initialize_db()

# Saves workouts to the database
def save_workout(workout):
    with sqlite3.connect('workout_storage.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO workouts VALUES (?, ?, ?, ?, ?)
        ''', (workout.exercise, workout.sets, workout.reps, workout.weight, workout.date))
        conn.commit()

# Loads workouts from the database
def load_workouts():
    with sqlite3.connect('workout_storage.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM workouts')
        rows = cursor.fetchall()
        el = []
        for row in rows:
                w = Workout(row[0], int(row[1]), int(row[2]), float(row[3]), (row[4]))
                el.append(w)
        return el