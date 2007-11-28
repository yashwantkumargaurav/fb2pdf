ALTER TABLE Books ADD COLUMN md5hash VARCHAR(32) NOT NULL AFTER md5_hash;

UPDATE Books SET md5hash = CONV(md5_hash, 10, 16);

ALTER TABLE Books ADD UNIQUE md5hash_uniq (md5hash);

ALTER TABLE Books DROP COLUMN md5_hash;

