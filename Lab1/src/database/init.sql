CREATE TABLE IF NOT EXISTS user_counter
(
    user_id integer PRIMARY KEY,
    counter integer NOT NULL,
    version integer
);
INSERT INTO user_counter VALUES (1, 0, 0);
