-- migrate:up

CREATE EXTENSION pgcrypto;
CREATE TABLE users
(
    id       uuid              DEFAULT gen_random_uuid() NOT NULL,
    username character varying                           NOT NULL,
    password character varying                           NOT NULL,
    CONSTRAINT users_pkey PRIMARY KEY (id)
);

-- migrate:down

DROP TABLE users;
DROP EXTENSION pgcrypto;
