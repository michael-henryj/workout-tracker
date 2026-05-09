import sqlite3
from workout import Workout

# When program is run the database is created or reinitialized
def initialize_db():
    with sqlite3.connect('workout_storage.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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
        INSERT INTO workouts VALUES (NULL, ?, ?, ?, ?, ?)
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
                w = Workout(row[1], int(row[2]), int(row[3]), float(row[4]), (row[5]), id = row[0])
                el.append(w)
        return el

# Deletes specific workouts using their unique ids
def delete_by_id(workout_id):
    with sqlite3.connect('workout_storage.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM workouts WHERE id = ?', (workout_id,))
        conn.commit()

# Will delete all workouts for a given day
def delete_by_date(workout_date):
    with sqlite3.connect('workout_storage.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM workouts WHERE date LIKE ?', (f"{workout_date}%",))
        conn.commit()

# Will completely reset the entire database
def delete_all():
    with sqlite3.connect('workout_storage.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM workouts')
        conn.commit()