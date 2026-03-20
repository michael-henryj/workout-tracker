# This program works in the console by presenting the user with a menu allowing them to choose between 4 preset options
# and being able to exit by choosing 5

#imports
from workout import Workout
from tracker import WorkoutTracker
from datetime import datetime

# functions for each menu option
def add_workout(tracker):
    exercise = input("What is the workout?\n")
    sets = int(input("How many sets will you do?\n"))
    reps = int(input("How many reps will you do?\n"))
    weight = float(input("At what weight will you complete the workout in lbs?\n"))
    date = datetime.now()
    new_workout = Workout(exercise, sets, reps, weight, date)
    tracker.add_workout(new_workout)

def load_workout(tracker):
    tracker.display_all()

def get_pr(tracker):
    exercise = input("Which workout would you like your PR for?\n")
    pr = tracker.get_pr(exercise)
    if pr is not None:
        print(f"{pr}\nThis is your best workout so far!!!")
    else:
        print("No saved workouts for this exercise.")

def get_volume(tracker):
    exercise = input("Which workout would you like your total volume for?\n")
    volume = tracker.total_volume(exercise)
    if volume is not None:
        print(f"{volume}\nThis is the total volume for this exercise")
    else:
        print("No saved workouts for this exercise.")

# This main function prints the menu and calls any functions necessary based on the users choice
def main():
    tracker = WorkoutTracker()
    while True:
        try:
            direction_choice = int(input(f'1. Add Workout \n2. Load Workout \n3. Get your personal record \n'
                                        f'4. Find your total volume\n5. Exit\n'))
            if direction_choice <= 0 or direction_choice > 5:
                raise ValueError
            else:
                # Input paths
                if direction_choice == 1:
                    add_workout(tracker)
                elif direction_choice == 2:
                    load_workout(tracker)
                elif direction_choice == 3:
                    get_pr(tracker)
                elif direction_choice == 4:
                    get_volume(tracker)
                else:
                    print("See you soon!")
                    break
        except ValueError:
            print("Invalid selection please try again.")


if __name__ == "__main__":
    main()
