import sqlite3
from flask import g, current_app
import click
import datetime
import os
import time


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            'railway.db', detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def trains_init():
    db = get_db()
    with open('train_data/Train.csv') as f:
        file = open('rrs.sql', 'a')
        for line in f.readlines()[1:]:
            data = line.strip().split(',')
            db.execute('INSERT INTO Trains(train_number,train_name,premium_fair,general_fair,source_station,destination_station) VALUES(?,?,?,?,?,?);',
                       (int(data[0]), data[1], float(data[2]), float(data[3]), data[4], data[5]))
            file.write(
                f'INSERT INTO Trains(train_number,train_name,premium_fair,general_fair,source_station,destination_station) VALUES({int(data[0])},{data[1]},{float(data[2])},{float(data[3])},{data[4]},{data[5]});')
            file.write('\n')
        file.write('\n')
        db.commit()
        file.close()


def train_status_init():
    db = get_db()
    with open('train_data/Train_status.csv') as f:
        file = open('rrs.sql', 'a')
        for line in f.readlines()[1:]:
            data = line.strip().split(',')
            db.execute('INSERT INTO Trains_Status(train_date,train_name,premium_seats_available,general_seats_available,premium_seats_occupied,general_seats_occupied) VALUES(?,?,?,?,?,?);',
                       (datetime.date.fromisoformat(data[0]), data[1], int(data[2]), int(data[3]), int(data[4]), int(data[5])))
            file.write('INSERT INTO Trains_Status(train_date,train_name,premium_seats_available,general_seats_available,premium_seats_occupied,general_seats_occupied) VALUES({0},{1},{2},{3},{4},{5});'.format(
                datetime.date.fromisoformat(data[0]), data[1], int(data[2]), int(data[3]), int(data[4]), int(data[5])))
            file.write('\n')
        file.write('\n')
        db.commit()
        file.close()


def passengers_init():
    db = get_db()
    with open('train_data/Passenger.csv') as f:
        file = open('rrs.sql', 'a')
        for line in f.readlines()[1:]:
            data = line.strip().split(',')
            date = data[7].split('/')
            if int(date[2]) > 23:
                date[2] = '19' + date[2]
            else:
                date[2] = '20' + date[2]
            data[7] = "/".join(date)
            db.execute('INSERT INTO Passengers(first_name,last_name,address,city,county,phone,ssn,bdate) VALUES (?,?,?,?,?,?,?,?);',
                       (data[0], data[1], data[2], data[3], data[4], data[5], data[6], datetime.datetime.strptime(data[7], '%m/%d/%Y').date()))
            file.write('INSERT INTO Passengers(first_name,last_name,address,city,county,phone,ssn,bdate) VALUES ({0},{1},{2},{3},{4},{5},{6},{7});'.format(
                data[0], data[1], data[2], data[3], data[4], data[5], data[6], datetime.datetime.strptime(data[7], '%m/%d/%Y').date()))
            file.write('\n')
        file.write('\n')
        db.commit()
        file.close()


def bookings_init():
    db = get_db()
    with open('train_data/booked.csv') as f:
        file = open('rrs.sql', 'a')
        for line in f.readlines()[1:]:
            data = line.strip().split(',')
            db.execute('INSERT INTO Bookings(passanger_ssn,train_Number,ticket_Type,status) VALUES (?,?,?,?);',
                       (data[0], int(data[1]), data[2], data[3]))
            file.write('INSERT INTO Bookings(passanger_ssn,train_Number,ticket_Type,status) VALUES ({},{},{},{});'.format(
                data[0], int(data[1]), data[2], data[3]))
            file.write('\n')
        file.write('\n')
        db.commit()
        file.close()


def init_db():
    db = get_db()
    with current_app.open_resource('app\\db\\railway_schema.sql') as f:
        if os.path.exists("rrs.sql"):
            os.remove("rrs.sql")
        content = f.read().decode('utf8')
        db.executescript(content)
        file = open('rrs.sql', 'a')
        file.write(content)
        file.write('\n')
        file.close()
    trains_init()
    train_status_init()
    passengers_init()
    bookings_init()
    if os.path.exists("rrs_backup.sql"):
        os.remove("rrs_backup.sql")
    with open("rrs_backup.sql", "w") as f:
        for line in db.iterdump():
            f.write('%s\n' % line)


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
