CREATE DATABASE RAILWAY_SYSTEM;
USE RAILWAY_SYSTEM;

DROP TABLE IF EXISTS Trains;
DROP TABLE IF EXISTS Trains_Status;
DROP TABLE IF EXISTS Passengers;
DROP TABLE IF EXISTS Bookings;

CREATE TABLE Trains (
    train_number INT PRIMARY KEY AUTO_INCREMENT=1,
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
    staus VARCHAR(255) NOT NULL,
    FOREIGN KEY (passanger_ssn) REFERENCES Passengers(ssn),
    FOREIGN KEY (train_Number) REFERENCES Trains(train_number)
);
SELECT * FROM Trains WHERE train_Number in (SELECT train_Number FROM Bookings WHERE passanger_ssn in (SELECT ssn FROM Passengers WHERE first_name = 'Art' and last_name = 'Venere'));