from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import login_required, current_user

from . import db
from .models import User, Workout

main = Blueprint('main', __name__)


# decorator
@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@main.route('/new')
@login_required
def new_workout():
    return render_template('create_workout.html')


@main.route('/new', methods=['POST'])
@login_required
def new_workout_post():
    pushups = request.form.get('pushups')
    comment = request.form.get('comment')

    workout = Workout(pushups=pushups, comment=comment, author=current_user)
    db.session.add(workout)
    db.session.commit()

    flash('Your Workout has been added')

    return redirect(url_for('main.user_workouts'))


@main.route('/all')
@login_required
def user_workouts():
    # this will take page number from url and displays respective page records
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(email=current_user.email).first_or_404()
    #without pagination
    #workouts = user.workouts
    #with pagination
    workouts = Workout.query.filter_by(author=user).paginate(page=page, per_page=3)
    #workout_paginate = Workout.query.filter_by(author=user).paginate(per_page=3)
    #print(dir(workout_paginate))
    #print(workout_paginate.items)
    #print(workout_paginate.page)
    return render_template('all_workouts.html', workouts=workouts, user=user)


@main.route('/workout/<int:workout_id>/update', methods=['GET', 'POST'])
@login_required
def update_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    if request.method == 'POST':
        workout.pushups = request.form['pushups']
        workout.comment = request.form['comment']
        db.session.commit()
        flash('Your Workout has been updated')
        return redirect(url_for('main.user_workouts'))
    return render_template('update_workout.html', workout=workout)

@main.route('/workout/<int:workout_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    db.session.delete(workout)
    db.session.commit()
    flash('Your Workout has been deleted')
    return redirect(url_for('main.user_workouts'))

