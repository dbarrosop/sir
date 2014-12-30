CREATE TABLE route_statistics
(
    time TEXT PRIMARY KEY NOT NULL,
    total INTEGER NOT NULL,
    kept INTEGER NOT NULL,
    removed INTEGER NOT NULL,
    added INTEGER NOT NULL
);
