
-- Catalog of the converted books
CREATE TABLE IF NOT EXISTS Books
(
        id          INT NOT NULL AUTO_INCREMENT,
        
        -- storage key of the converted book
        storage_key VARCHAR(32)  NOT NULL,
        
        -- book info 
        author      VARCHAR(128) NULL,
        title       VARCHAR(256) NULL,
        
        -- conversion status (TRUE - ready, FALSE - not ready)
        status      BOOL DEFAULT 0,
        
        INDEX   storage_key_idx (storage_key),
        INDEX   author_idx (author),
        
        UNIQUE  storage_key_uniq (storage_key),
        
        PRIMARY KEY(id)
) TYPE=INNODB;

