
-- Catalog of the converted books
CREATE TABLE IF NOT EXISTS Books
(
        id          INT NOT NULL AUTO_INCREMENT,
        
        -- storage key of the converted book
        storage_key VARCHAR(64)  NOT NULL,
        
        -- book info 
        author      VARCHAR(128) NULL,
        title       VARCHAR(256) NULL,
        isbn        VARCHAR(16)  NULL,
        
        -- md5 of the book's content
        md5hash     VARCHAR(32)  NOT NULL,
        
        -- conversion status ('r' - ready, 'e' - error, 'p' - processing)
        status      CHAR(1) DEFAULT NULL,
        converted   DATETIME NULL,
        counter     INT DEFAULT 0 NOT NULL,
        conv_ver    FLOAT DEFAULT '0' NOT NULL,
        
        INDEX   storage_key_idx (storage_key),
        INDEX   author_idx (author),
        INDEX   converted_idx (converted),
        INDEX   counter_idx (counter),
        
        UNIQUE  storage_key_uniq (storage_key),
        UNIQUE  md5hash_uniq (md5hash),
        
        PRIMARY KEY(id)
) TYPE=INNODB;

