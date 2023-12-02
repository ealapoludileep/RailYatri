CREATE DATABASE RAILWAY_SYSTEM;
USE RAILWAY_SYSTEM;

DROP TABLE IF EXISTS Trains;
DROP TABLE IF EXISTS Trains_Status;
DROP TABLE IF EXISTS Passengers;
DROP TABLE IF EXISTS Bookings;

CREATE TABLE Trains (
    train_number INT PRIMARY KEY,
    train_name VARCHAR(255) NOT NULL UNIQUE,
    premium_fair INT NOT NULL,
    general_fair INT NOT NULL,
    source_station VARCHAR(255) NOT NULL,
    destination_station VARCHAR(255) NOT NULL
);

CREATE TABLE Trains_Status (
    train_date datetime NOT NULL,
    train_name VARCHAR(255) NOT NULL,
    premium_seats_available INT NOT NULL,
    general_seats_available INT NOT NULL,
    premium_seats_occupied INT NOT NULL,
    general_seats_occupied INT NOT NULL,
    CONSTRAINT compositeKey PRIMARY KEY (train_date, train_name),
    FOREIGN KEY (train_name) REFERENCES Trains(train_name)
);

CREATE TABLE Passengers (
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    address VARCHAR(255),
    city VARCHAR(255),
    county VARCHAR(255),
    phone VARCHAR(255),
    ssn VARCHAR(255) PRIMARY KEY NOT NULL,
    bdate datetime NOT NULL
);

CREATE TABLE Bookings (
    passanger_ssn VARCHAR(255) PRIMARY KEY NOT NULL,
    train_Number INT NOT NULL,
    ticket_Type VARCHAR(255) NOT NULL,
    status VARCHAR(255) NOT NULL,
    FOREIGN KEY (passanger_ssn) REFERENCES Passengers(ssn),
    FOREIGN KEY (train_Number) REFERENCES Trains(train_number)
);
-- SELECT * FROM Trains WHERE train_Number in (SELECT train_Number FROM Bookings WHERE passanger_ssn in (SELECT ssn FROM Passengers WHERE first_name = 'Art' and last_name = 'Venere'));
-- SELECT * FROM Passengers AS p INNER JOIN Bookings AS b ON p.ssn = b.passanger_ssn and b.train_Number in (SELECT train_number FROM Trains WHERE train_name in (SELECT train_name FROM Trains_Status WHERE train_date = '2022-02-21'));

-- SELECT * FROM Bookings AS b INNER JOIN Trains as t ON b.train_number = t.train_number;

-- SELECT * FROM Passengers AS p INNER JOIN (SELECT * FROM Bookings AS b INNER JOIN Trains as t ON b.train_number = t.train_number) AS b ON p.ssn = b.passanger_ssn and b.train_Number in (SELECT train_number FROM Trains WHERE train_name in (SELECT train_name FROM Trains_Status WHERE train_date = '2022-02-22')) and b.status != 'WaitL';

-- SELECT * FROM Trains AS t INNER JOIN Trains_Status AS ts ON t.train_name = ts.train_name GROUP BY ts.train_date ORDER BY train_date;

-- SELECT DISTINCT(train_name) FROM Trains;

-- SELECT * FROM Bookings AS b INNER JOIN Passengers AS p ON b.passanger_ssn = p.ssn WHERE b.train_Number in (SELECT train_number FROM Trains WHERE train_name = 'Golden Chariot') AND b.status = 'Booked' ORDER BY b.train_number;

-- SELECT * FROM Bookings WHERE passanger_ssn = '' AND train_Number in (SELECT train_id FROM Trains WHERE train_name = '');

-- DELETE FROM Bookings WHERE passger_ssn = '' AND train_Number in  (SELECT train_id FROM Trains WHERE train_name = '');

-- SELECT passenger_ssn FROM Bookings WHERE train_Number in  (SELECT train_id FROM Trains WHERE train_name = '') and status = 'WaitL' LIMIT 1;

-- UPDATE Bookings SET status = 'Booked' WHERE passenger_ssn = ? AND train_Number in  (SELECT train_id FROM Trains WHERE train_name =  ?)

-- SELECT * FROM Passengers WHERE ssn = ?;

-- SELECT t.train_number,t.train_name, t.source_station, t.destination_station, CONCAT(p.first_name, ' ', p.last_name) as Name, p.address, b.ticket_Type as category, b.status as status, DATEDIFF(hour,p.bdate,GETDATE())/8766 AS age FROM Trains AS t JOIN Bookings AS b ON b.train_Number = t.train_number Join Passengers AS p ON p.ssn = b.passanger_ssn WHERE age BETWEEN ? AND ? ORDER BY age; 

-- SELECT * FROM Passengers AS p INNER JOIN (SELECT * FROM Bookings AS b INNER JOIN Trains as t ON b.train_number = t.train_number) AS b ON p.ssn = b.passanger_ssn WHERE b.train_Number in (SELECT train_number FROM Trains WHERE train_name in (SELECT train_name FROM Trains_Status WHERE train_date = \''+date+'\')) and b.status != \'WaitL\';