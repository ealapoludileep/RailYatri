from flask import Flask, g, render_template, Blueprint, flash, request, redirect, url_for
from .db.init import get_db
import datetime

bp = Blueprint('railway', __name__, url_prefix='/railway')


@bp.route('/')
def index():
    return render_template('railway/index.html')


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


@bp.route('/confirmed_passengers', methods=['GET', 'POST'])
def get_confirmed_passengers():
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    if request.method == 'POST':
        date = datetime.datetime.strptime(
            request.form['date'], '%Y-%m-%d').strftime("%Y-%m-%d")
    db = get_db()
    print(date)
    passengers = db.execute('SELECT * FROM Passengers AS p INNER JOIN (SELECT * FROM Bookings AS b INNER JOIN Trains as t ON b.train_number = t.train_number) AS b ON p.ssn = b.passanger_ssn WHERE b.train_Number in (SELECT train_number FROM Trains WHERE train_name in (SELECT train_name FROM Trains_Status WHERE train_date = \''+date+'\')) and b.staus != \'WaitL\';').fetchall()
    print(passengers)
    return render_template('railway/booked_passengers.html', max_date=datetime.datetime.now(), date=date, passengers=passengers)


@bp.route('train_status', methods=['GET', 'POST'])
def get_train_status():
    db = get_db()
    trains = db.execute(
        'SELECT * FROM Trains_Status AS ts JOIN Trains AS t WHERE t.train_name = ts.train_name ORDER BY train_date DESC;').fetchall()
    trains_dict = {}
    for train in trains:
        train = dict(train)
        if train['train_date'] not in trains_dict:
            trains_dict[str(train['train_date'])] = [train]
        else:
            trains_dict[str(train['train_date'])].append(train)

    return render_template('railway/trains.html', trains=trains_dict)
