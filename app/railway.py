from flask import Flask, g, render_template, Blueprint, flash, request, redirect, url_for
from .db.init import get_db

bp = Blueprint('railway', __name__)


@bp.route('/')
def index():
    return render_template('base.html')


@bp.route('/booked_trains', methods=['GET', 'POST'])
def booked_trains():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        error = None
        if not first_name:
            error = 'First name must be provided'
        if not last_name:
            error = 'Last name must be provided'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            trains = db.execute(
                'SELECT * FROM Trains WHERE train_Number in (SELECT train_Number FROM Bookings WHERE passanger_ssn in (SELECT ssn FROM Passengers WHERE first_name = ? and last_name = ?));', (first_name, last_name)).fetchall()
            return render_template('railway/bookings.html', trains=trains)
    return render_template('railway/bookings.html')
