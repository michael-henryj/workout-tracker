import sqlite3
from workout import Workout
from models import User

# When program is run the database is created or reinitialized
def initialize_db():
    with sqlite3.connect('workout_storage.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER REFERENCES users(id),
            exercise TEXT,
            sets INTEGER,
            reps INTEGER,
            weight REAL,
            date TEXT
        )
        ''')
        conn.commit()

initialize_db()

# User table is created allowing the user to sign up
def initialize_users_table():
    with sqlite3.connect('workout_storage.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT
        )
        ''')
        conn.commit()

initialize_users_table()

# Users profile created to store users body info
def initialize_user_profiles_table():
    with sqlite3.connect('workout_storage.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_profiles (
            user_id INTEGER REFERENCES users(id),
            height INTEGER,
            weight INTEGER,
            age INTEGER,
            gender TEXT
        )
        ''')
        conn.commit()

initialize_user_profiles_table()

# Saves users to the database
def save_user(username, email, password_hash):
    from datetime import datetime
    with sqlite3.connect('workout_storage.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO users (username, email, password_hash, created_at)
        VALUES (?, ?, ?, ?)
        ''', (username, email, password_hash, str(datetime.now()))
        )
        conn.commit()

# Finds users by their usernames
def get_user_by_username(username):
    from models import User
    with sqlite3.connect('workout_storage.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        row = cursor.fetchone()
        if row:
            return User(row[0], row[1], row[2], row[3])
        return None

# Finds users by their id
def get_user_by_id(user_id):
    from models import User
    with sqlite3.connect('workout_storage.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        row = cursor.fetchone()
        if row:
            return User(row[0], row[1], row[2], row[3])
        return None

# Saves user profiles
def save_user_profile(user_id, height, weight, age, gender):
    with sqlite3.connect('workout_storage.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO user_profiles(user_id, height, weight, age, gender)
        VALUES(?, ?, ?, ?, ?)
        ''', (user_id, height, weight, age, gender))
        conn.commit()

# Loads a users profile based on the user id
def load_user_profile(user_id):
    with sqlite3.connect('workout_storage.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM user_profiles WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        if row:
            return {
                'user_id': row[0],
                'height': row[1],
                'weight': row[2],
                'age': row[3],
                'gender': row[4]
            }
        return None


# Saves workouts to the database
def save_workout(workout, user_id):
    with sqlite3.connect('workout_storage.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO workouts VALUES (NULL, ?, ?, ?, ?, ?, ?)
        ''', (user_id, workout.exercise, workout.sets, workout.reps, workout.weight, workout.date))
        conn.commit()

# Loads workouts from the database
def load_workouts(user_id):
    with sqlite3.connect('workout_storage.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM workouts WHERE user_id = ?', (user_id,))
        rows = cursor.fetchall()
        el = []
        for row in rows:
                w = Workout(row[2], int(row[3]), int(row[4]), float(row[5]), (row[6]),user_id = row[1], id = row[0])
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
def delete_all(user_id):
    with sqlite3.connect('workout_storage.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM workouts WHERE user_id = ?', (user_id,))
        conn.commit()