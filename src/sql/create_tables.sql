
-- Catalog of the converted books
CREATE TABLE IF NOT EXISTS Books
(
        id          INT NOT NULL AUTO_INCREMENT,
        
        -- storage key of the converted book
        storage_key VARCHAR(32)  NOT NULL,
        
        -- book info 
        author      VARCHAR(128) NULL,
        title       VARCHAR(256) NULL,
        
        -- md5 of the book's content
        md5_hash    BIGINT UNSIGNED NOT NULL,
        
        -- conversion status ('r' - ready, 'e' - error)
        status      CHAR(1) DEFAULT NULL,
        
        INDEX   storage_key_idx (storage_key),
        INDEX   author_idx (author),
        INDEX   md5_hash_idx (md5_hash),
        
        UNIQUE  storage_key_uniq (storage_key),
        UNIQUE  md5_hash_uniq (md5_hash),
        
        PRIMARY KEY(id)
) TYPE=INNODB;

