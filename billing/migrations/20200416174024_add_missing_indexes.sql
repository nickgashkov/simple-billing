-- migrate:up

CREATE INDEX operations_id_timestamp_idx ON operations(wallet_id, timestamp);
CREATE INDEX wallets_user_id_idx ON wallets(user_id);

-- migrate:down

DROP INDEX wallets_user_id_idx;
DROP INDEX operations_id_timestamp_idx;
