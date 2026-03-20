from storage import save_workout, load_workouts

class WorkoutTracker:
    def __init__(self):
        self.workouts = []
        self.load_all()

    # Function creates a workout object then saves it to the SQLite database
    def add_workout(self, workout):
        self.workouts.append(workout)
        save_workout(workout)

    # Function unnecessary with the use of a SQLite database
    def load_all(self):
        self.workouts = load_workouts()

    # Function unnecessary with the use of a SQLite database
    def display_all(self):
        if not self.workouts:
            print("You have not saved any workouts yet.")
        else:
            for workout in self.workouts:
                print(f"{workout.date} | {workout.exercise} | {workout.sets} sets | {workout.reps} reps | {workout.weight} lbs")

    # Function sorts through all exercises by name and is not case-sensitive
    def get_by_exercise(self, exercise_name):
        return [workout for workout in self.workouts if workout.exercise.lower() == exercise_name.lower()]

    # Method sorts all of a specific exersice to find the one with the highest weight
    def get_pr(self, exercise_name):
        all_workouts = self.get_by_exercise(exercise_name)
        if not all_workouts:
            return None
        else:
            pr = max(all_workouts, key= lambda workout: workout.weight)
            return pr

    # Method find the total volume of any given exercise, still not sure of its practical use
    def total_volume(self, exercise_name):
        all_workouts = self.get_by_exercise(exercise_name)
        if not all_workouts:
            return None
        else:
            return sum(workout.sets * workout.reps * workout.weight for workout in all_workouts)

    # Method changes workouts into a dictionary for json
    def get_all(self):
        return [w.to_dict() for w in self.workouts]