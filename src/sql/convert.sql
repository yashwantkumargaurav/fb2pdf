-- SQL script to convert from old to new db schema

TRUNCATE OriginalBooks;
TRUNCATE ConvertedBooks;
TRUNCATE TitleSearch;
TRUNCATE AuthorSearch;

INSERT INTO OriginalBooks (id, storage_key, author, title, isbn, md5hash, submitted, valid)
       SELECT id, REPLACE(storage_key, '.zip', ''), author, title, isbn, md5hash, converted, status="r" FROM Books;

INSERT INTO ConvertedBooks (book_id, format, status, converted, counter, conv_ver)
       SELECT id, 1, status, converted, counter, conv_ver FROM Books;

INSERT INTO TitleSearch (book_id, title) 
       SELECT id, title FROM Books;

INSERT INTO AuthorSearch (author) 
       SELECT DISTINCT author FROM Books;
