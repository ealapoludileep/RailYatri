DROP TABLE IF EXISTS Trains;
DROP TABLE IF EXISTS Trains_Status;
DROP TABLE IF EXISTS Passengers;
DROP TABLE IF EXISTS Bookings;

CREATE TABLE Trains (
    train_number INT AUTO_INCREMENT PRIMARY KEY,
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
    passanger_ssn VARCHAR(255) NOT NULL,
    train_Number INT NOT NULL,
    ticket_Type VARCHAR(255) NOT NULL,
    status VARCHAR(255) NOT NULL,
    FOREIGN KEY (passanger_ssn) REFERENCES Passengers(ssn),
    FOREIGN KEY (train_Number) REFERENCES Trains(train_number)
);

-- Question 2 Subquery
-- SELECT t.train_number FROM Trains_Status AS ts JOIN Trains AS t ON ts.train_name = t.train_name WHERE ts.train_date = '2022-02-19';

-- Question 2
-- SELECT (p.first_name|| " "||p.last_name) AS full_name FROM Bookings AS b JOIN Trains as t ON b.train_Number = t.train_number JOIN Passengers as p ON p.ssn = b.passanger_ssn WHERE b.status = 'Booked' AND t.train_number in (SELECT t.train_number FROM Trains_Status AS ts JOIN Trains AS t ON ts.train_name = t.train_name WHERE ts.train_date = '2022-02-19');

-- Question 3
-- SELECT t.train_number,t.train_name, t.source_station, t.destination_station, p.first_name, p.last_name, p.address, b.ticket_Type as category, b.status as status, cast(strftime('%Y', 'now') - strftime('%Y', bdate) as int)  AS age FROM Trains AS t JOIN Bookings AS b ON b.train_Number = t.train_number Join Passengers AS p ON p.ssn = b.passanger_ssn WHERE age BETWEEN 50 AND 60 ORDER BY age;

-- Question 1
-- SELECT DISTINCT(t.train_name) FROM (Passengers as p INNER JOIN Bookings AS b ON p.ssn = b.passanger_ssn) INNER JOIN Trains AS t ON b.train_Number = t.train_number WHERE p.first_name = '' AND p.last_name = '';

-- Question 4
-- SELECT train_name, train_date, (premium_seats_occupied+general_seats_occupied) AS passengers_count FROM Trains_Status;

-- Question 5
-- SELECT (p.first_name ||' ' || p.last_name) AS full_name FROM Passengers as p JOIN Bookings as b ON p.ssn = b.passanger_ssn JOIN Train as t ON b.train_Number = t.train_number WHERE t.train_name = '' AND b.status = 'Booked';

-- Question 6 Get passgener details
-- SELECT * FROM Bookings WHERE status = 'Booked' AND passanger_ssn = '' AND train_Number = '' AND ticket_Type = '';

-- Question 6 Delete passgener booking if exists
-- DELETE FROM Bookings WHERE status = 'Booked' AND passanger_ssn = '' AND train_Number = '' AND ticket_Type = '';

-- Question 6 get next passenger on wailtlist
-- SELECT * FROM Bookings WHERE status = 'WaitL' AND train_Number = '' AND ticket_Type = 'Premium' LIMIT 1;

-- Question 6 update next passenger on wailtlist
-- UPDATE Bookings SET status = "Booked" WHERE status = 'WaitL' AND passanger_ssn = '' AND train_Number = '' AND ticket_Type = '';