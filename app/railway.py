from flask import Flask, g, render_template, Blueprint, flash, request, redirect, url_for
from .db.init import get_db, init_db
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
    passengers = db.execute('SELECT * FROM Passengers AS p INNER JOIN (SELECT * FROM Bookings AS b INNER JOIN Trains as t ON b.train_number = t.train_number) AS b ON p.ssn = b.passanger_ssn WHERE b.train_Number in (SELECT train_number FROM Trains WHERE train_name in (SELECT train_name FROM Trains_Status WHERE train_date = \''+date+'\')) and b.staus != \'WaitL\';').fetchall()
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


@bp.route('/train_passengers', methods=['POST', 'GET'])
def get_train_passengers():
    db = get_db()
    trains = db.execute('SELECT DISTINCT(train_name) FROM Trains;').fetchall()
    train_name = dict(trains[0])['train_name']
    if request.method == 'POST':
        train_name = request.form['train_name']
    train_passengers = db.execute(
        "SELECT * FROM Bookings AS b INNER JOIN Passengers AS p ON b.passanger_ssn = p.ssn WHERE b.train_Number in (SELECT train_number FROM Trains WHERE train_name = ?) AND b.staus = 'Booked' ORDER BY p.first_name;", (train_name,)).fetchall()
    return render_template('railway/train_passengers.html', train_name=train_name, trains=trains, train_passengers=train_passengers)


@bp.route('/passengers_by_age', methods=['POST', 'GET'])
def get_passengers_by_age():
    age_from = 0
    age_to = 100
    db = get_db()
    if request.method == 'POST':
        age_from = int(request.form['age_from'])
        age_to = int(request.form['age_to'])
    passengers = db.execute('SELECT t.train_number,t.train_name, t.source_station, t.destination_station, p.first_name, p.last_name, p.address, b.ticket_Type as category, b.staus as status, cast(strftime(\'%Y.%m%d\', \'now\') - strftime(\'%Y.%m%d\', bdate) as int)  AS age FROM Trains AS t JOIN Bookings AS b ON b.train_Number = t.train_number Join Passengers AS p ON p.ssn = b.passanger_ssn WHERE age BETWEEN ? AND ? ORDER BY age; ', (age_from, age_to,)).fetchall()
    return render_template('railway/passengers_by_age.html', age_from=age_from, age_to=age_to, passengers=passengers)


@bp.route('/cancel_ticket', methods=['POST', 'GET'])
def cancel_ticket():
    db = get_db()
    found_passanger = False
    found_next_passanger = False
    next_passenger_ssn = None
    passanger = []
    cancled_passanger = []
    post_request = False
    trains = db.execute('SELECT DISTINCT(train_name) FROM Trains;').fetchall()
    train_name = dict(trains[0])['train_name']
    if request.method == 'POST':
        post_request = True
        train_name = request.form['train_name']
        passenger_ssn = request.form['passanger_ssn']
        train_name = request.form['train_name']
        selected_trains = db.execute('SELECT * FROM Bookings WHERE passanger_ssn = ? AND train_Number in (SELECT train_number FROM Trains WHERE train_name = ?);',
                                     (passenger_ssn, train_name)).fetchall()
        if len(selected_trains) > 0:
            db.execute(
                'DELETE FROM Bookings WHERE passanger_ssn = ? AND train_Number in  (SELECT train_number FROM Trains WHERE train_name = ?);', (passenger_ssn, train_name))
            db.commit()
            cancled_passanger = db.execute('SELECT * FROM Passengers WHERE ssn = ?;',
                                           (passenger_ssn,)).fetchall()
            found_passanger = True
            next_passenger = db.execute(
                'SELECT passanger_ssn FROM Bookings WHERE train_Number in  (SELECT train_number FROM Trains WHERE train_name = ?) and staus = \'WaitL\' LIMIT 1;', (train_name,)).fetchall()
            if len(next_passenger) != 0:
                next_passenger_ssn = dict(next_passenger[0])['passanger_ssn']
                db.execute('UPDATE Bookings SET staus = \'Booked\' WHERE passanger_ssn = ? AND train_Number in  (SELECT train_number FROM Trains WHERE train_name =  ?);',
                           (next_passenger_ssn, train_name))
                db.commit()
                found_next_passanger = True
                passanger = db.execute('SELECT * FROM Passengers WHERE ssn = ?;',
                                       (next_passenger_ssn,)).fetchall()
    return render_template('railway/cancel_ticket.html', trains=trains, train_name=train_name, found_passanger=found_passanger, found_next_passanger=found_next_passanger, passanger=passanger, post_request=post_request, cancled_passanger=cancled_passanger)


@bp.route('reset-db', methods=['GET'])
def reset_db():
    init_db()
    return {"message": "Successfully reseted the database"}
