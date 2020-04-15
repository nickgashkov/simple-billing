-- migrate:up

CREATE TABLE wallets
(
    id      uuid DEFAULT gen_random_uuid() NOT NULL,
    user_id uuid REFERENCES users(id)       NOT NULL,
    CONSTRAINT wallets_pkey PRIMARY KEY (id)
);

CREATE TABLE operations
(
    id                    uuid              DEFAULT gen_random_uuid()  NOT NULL,
    wallet_id             uuid              REFERENCES wallets(id)     NOT NULL,
    source_wallet_id      uuid              REFERENCES wallets(id)             ,
    destination_wallet_id uuid              REFERENCES wallets(id)     NOT NULL,
    type                  character varying                            NOT NULL,
    amount                numeric(1000, 2)                             NOT NULL,
    timestamp             timestamp                                    NOT NULL,
    CONSTRAINT operations_pkey PRIMARY KEY (id)
);

-- migrate:down

DROP TABLE operations;
DROP TABLE wallets;
