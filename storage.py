#import csv
import sqlite3
from workout import Workout

# def save_workout(workout):
#     with open('workout_storage.csv', mode='a', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow([
#             workout.date,
#             workout.exercise,
#             workout.sets,
#             workout.reps,
#             workout.weight
#         ])
#         print("Your workout has been saved!")
#
# def load_workouts():
#     el = []
#     try:
#         with open('workout_storage.csv', mode='r', encoding= 'utf-8') as file:
#             reader = csv.reader(file)
#             for row in reader:
#                 w = Workout(date= row[0], exercise= row[1], sets= int(row[2]), reps=int(row[3]), weight= float(row[4]))
#                 el.append(w)
#             return el
#
#     except FileNotFoundError:
#         return el

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

def save_workout(workout):
    with sqlite3.connect('workout_storage.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO workouts VALUES (?, ?, ?, ?, ?)
        ''', (workout.exercise, workout.sets, workout.reps, workout.weight, workout.date))
        conn.commit()

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