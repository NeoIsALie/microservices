CREATE TABLE flight
(
    id              SERIAL PRIMARY KEY,
    flight_number   VARCHAR(20)              NOT NULL,
    datetime        TIMESTAMP WITH TIME ZONE NOT NULL,
    from_airport_id INT REFERENCES airport (id),
    to_airport_id   INT REFERENCES airport (id),
    price           INT                      NOT NULL
);

CREATE TABLE airport
(
    id      SERIAL PRIMARY KEY,
    iata    VARCHAR(3),
    name    VARCHAR(255),
    city    VARCHAR(255),
    country VARCHAR(255)
);