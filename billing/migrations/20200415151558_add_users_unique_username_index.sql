-- migrate:up

CREATE UNIQUE INDEX users_username_idx ON users(username);

-- migrate:down

DROP INDEX users_username_idx;
