from flask import Flask, jsonify, request
from tracker import WorkoutTracker
from workout import Workout
from datetime import datetime

app = Flask(__name__)
tracker = WorkoutTracker()

@app.route('/workouts', methods=['GET'])
def get_workouts():
    return jsonify(tracker.get_all())

@app.route('/workouts', methods= ['POST'])
def add_workout():
    data = request.get_json()
    w = Workout(data["exercise"], data["sets"], data["reps"], data["weight"], date= datetime.now())
    tracker.add_workout(w)
    return jsonify({'message' : 'Workout saved!'})

@app.route('/workouts/pr/<exercise>', methods=['GET'])
def get_pr(exercise):
    pr = tracker.get_pr(exercise)
    if pr is None:
       return jsonify({'message': 'No past workouts for this exercise'}), 404
    pr_dict = pr.to_dict()
    return jsonify(pr_dict)

@app.route('/workouts/volume/<exercise>', methods=['GET'])
def get_volume(exercise):
    volume = tracker.total_volume(exercise)
    if volume is None:
        return jsonify({'message': 'No past workouts for this exercise'}), 404
    return jsonify(volume)

if __name__ == "__main__":
    app.run(debug=True)