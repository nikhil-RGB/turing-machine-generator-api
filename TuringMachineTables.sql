DROP TABLE IF EXISTS machines;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id SERIAL,
    username varchar(45) NOT NULL UNIQUE,
    hashed_password varchar(200) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE machines (
    id SERIAL,
    owner_id integer NOT NULL,
    name varchar(200) NOT NULL,
    machine_data TEXT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (owner_id) REFERENCES users(id)
);