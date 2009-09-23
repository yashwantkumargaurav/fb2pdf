
-- Catalog of all  books
-- This table refers to FB2 originals, which might be converted
-- into multiple formats.
CREATE TABLE IF NOT EXISTS OriginalBooks
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

        -- When book was submitted
        submitted   DATETIME NULL,

        -- whenever this books is valid
        -- The book is marked valid if it have been processed
        -- by backend at least once.
        valid      BOOLEAN DEFAULT FALSE,

        INDEX   storage_key_idx (storage_key),
        INDEX   author_idx (valid, author),
        INDEX   valid_idx (valid),
        
        UNIQUE  storage_key_uniq (storage_key),
        UNIQUE  md5hash_uniq (md5hash),
        
        PRIMARY KEY(id)
) TYPE=INNODB;

-- This table contains list of supported destination device formats,
-- such as Sony Reader, JetBook, iPhone, etc.
CREATE TABLE IF NOT EXISTS Formats
(
        id INT NOT NULL AUTO_INCREMENT,

        -- Human-readable format name, as shwon to the users.
        -- e.g. Sony Reader, JetBook, iPhone, etc.
        title VARCHAR(128) NOT NULL,

        -- (optional) brief format description which might be shown to the user
        description VARCHAR(256) NULL,


        PRIMARY KEY(id)
) TYPE=INNODB;

-- This table contains set of parameters for given format
CREATE TABLE IF NOT EXISTS FormatParams
(
        id INT NOT NULL AUTO_INCREMENT,

        format INT NOT NULL,

        -- param name
        name VARCHAR(64) NOT NULL,
        -- param value
        value VARCHAR(256) NOT NULL,

        UNIQUE  format_param_uniq (format, name),
        FOREIGN KEY(format) REFERENCES  Formats(id) ON UPDATE CASCADE ON DELETE CASCADE,
        PRIMARY KEY(id)
) TYPE=INNODB;

CREATE TABLE IF NOT EXISTS ConvertedBooks
(
        id INT NOT NULL AUTO_INCREMENT,

        book_id INT NOT NULL,
        format  INT NOT NULL,

        -- conversion status ('r' - ready, 'e' - error, 'p' - processing)
        status      CHAR(1) DEFAULT NULL,
        converted   DATETIME NULL,
        counter     INT DEFAULT 0 NOT NULL,
        conv_ver    FLOAT DEFAULT '0' NOT NULL,

        INDEX   converted_idx (converted),
        INDEX   counter_idx (counter),
        FOREIGN KEY(format) REFERENCES  Formats(id) ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY(book_id) REFERENCES OriginalBooks(id)   ON UPDATE CASCADE ON DELETE CASCADE,
        PRIMARY KEY(id)

) TYPE=INNODB;


CREATE TABLE IF NOT EXISTS TitleSearch 
(
       id INT NOT NULL AUTO_INCREMENT ,
       book_id INT NOT NULL ,
       title VARCHAR( 256 ) ,
       PRIMARY KEY ( id ) ,
       FULLTEXT (title)
) ENGINE = MYISAM CHARACTER SET utf8 COLLATE utf8_general_ci;

CREATE TABLE IF NOT EXISTS AuthorSearch 
(
       id INT NOT NULL AUTO_INCREMENT ,
       author VARCHAR( 256 ) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
       PRIMARY KEY ( id ) ,
       FULLTEXT (author) ,
       UNIQUE (author)
) ENGINE = MYISAM CHARACTER SET utf8 COLLATE utf8_general_ci;

