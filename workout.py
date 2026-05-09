class Workout:
    def __init__(self, exercise, sets, reps, weight, date, id = None, user_id = None):
        self.id = id
        self.user_id = user_id
        self.exercise = exercise
        self.sets = sets
        self.reps = reps
        self.weight = weight
        self.date = date

    def __str__(self):
        return f"{self.date} | {self.exercise} | {self.sets} sets | {self.reps} reps | {self.weight} lbs"

    def to_dict(self):
        return {'id': self.id, 'exercise': self.exercise, 'sets': self.sets, 'reps': self.reps, 'weight': self.weight,
                'date': self.date}