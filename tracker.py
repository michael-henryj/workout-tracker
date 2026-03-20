from storage import save_workout, load_workouts

#claudeai about to expand on the class to add workouts, load all workouts, find specific exercises, find prs, and a volume
class WorkoutTracker:
    def __init__(self):
        self.workouts = []
        self.load_all()

    def add_workout(self, workout):
        self.workouts.append(workout)
        save_workout(workout)

    def load_all(self):
        self.workouts = load_workouts()

    def display_all(self):
        if not self.workouts:
            print("You have not saved any workouts yet.")
        else:
            for workout in self.workouts:
                print(f"{workout.date} | {workout.exercise} | {workout.sets} sets | {workout.reps} reps | {workout.weight} lbs")

    def get_by_exercise(self, exercise_name):
        return [workout for workout in self.workouts if workout.exercise.lower() == exercise_name.lower()]
        #for workout in self.workouts:
            #if workout.exercise.lower() == exercise_name.lower():
                #same_exercise.append(workout)
        #return same_exercise
    def get_pr(self, exercise_name):
        all_workouts = self.get_by_exercise(exercise_name)
        if not all_workouts:
            return None
        else:
            pr = max(all_workouts, key= lambda workout: workout.weight)
            return pr

    def total_volume(self, exercise_name):
        all_workouts = self.get_by_exercise(exercise_name)
        if not all_workouts:
            return None
        else:
            return sum(workout.sets * workout.reps * workout.weight for workout in all_workouts)