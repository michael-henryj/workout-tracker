from flask import Flask, jsonify, request, render_template
from flask_login import LoginManager, login_required, current_user
from tracker import WorkoutTracker
from workout import Workout
from datetime import datetime
from flask_cors import CORS
from models import User
from storage import get_user_by_id
from auth import auth
app = Flask(__name__)
app.secret_key = 'secret_key'
CORS(app)


# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)

# Register the auth blueprint
app.register_blueprint(auth)

# Shows all the saved workouts in the database
@app.route('/workouts', methods=['GET'])
@login_required
def get_workouts():
    tracker = WorkoutTracker(current_user.id)
    return jsonify(tracker.get_all())

# Allows a user to input their workouts
@app.route('/workouts', methods= ['POST'])
@login_required
def add_workout():
    tracker = WorkoutTracker(current_user.id)
    data = request.get_json()
    sets = int(data["sets"])
    reps = int(data["reps"])
    weight = float(data["weight"])
    if sets <= 0:
        return jsonify({'message': 'Please enter a positive amount of sets.'}), 400
    if reps <= 0:
        return jsonify({'message': 'Please enter a positive amount of reps.'}), 400
    if weight <= 0:
        return jsonify({'message': 'Please enter a real weight.'}), 400
    w = Workout(data["exercise"], sets, reps, weight, date= datetime.now())
    tracker.add_workout(w, current_user.id)
    return jsonify({'message' : 'Workout saved!'})

# Deletes by exercise ID
@app.route('/workouts/<int:id>', methods=['DELETE'])
@login_required
def delete_workout(id):
    tracker = WorkoutTracker(current_user.id)
    tracker.delete_id(id, current_user.id)
    return jsonify({'message': 'Workout deleted!'})

# Deletes by date
@app.route('/workouts/date/<date>', methods=['DELETE'])
@login_required
def delete_date(date):
    tracker = WorkoutTracker(current_user.id)
    tracker.delete_date(date, current_user.id)
    return jsonify({'message': f'Workouts for {date} deleted!'})

# RESETS the db
@app.route('/workouts/all', methods=['DELETE'])
@login_required
def delete_all():
    tracker = WorkoutTracker(current_user.id)
    tracker.reset(current_user.id)
    return jsonify({'message': f'All workouts have been deleted!'})


# Shows the Personal Record exercise
@app.route('/workouts/pr/<exercise>', methods=['GET'])
@login_required
def get_pr(exercise):
    tracker = WorkoutTracker(current_user.id)
    pr = tracker.get_pr(exercise)
    if pr is None:
       return jsonify({'message': 'No past workouts for this exercise'}), 404
    pr_dict = pr.to_dict()
    return jsonify(pr_dict)

# Shows total volume with different exercises
@app.route('/workouts/volume/<exercise>', methods=['GET'])
@login_required
def get_volume(exercise):
    tracker = WorkoutTracker(current_user.id)
    volume = tracker.total_volume(exercise)
    if volume is None:
        return jsonify({'message': 'No past workouts for this exercise'}), 404
    return jsonify(volume)

@app.route("/")
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)