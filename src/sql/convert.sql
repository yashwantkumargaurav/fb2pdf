-- SQL script to convert from old to new db schema

DELETE FROM OriginalBooks;
DELETE FROM ConvertedBooks;

INSERT INTO OriginalBooks (id, storage_key, author, title, isbn, md5hash, submitted, valid)
       SELECT id, storage_key, author, title, isbn, md5hash, converted, status="r" FROM Books;

INSERT INTO ConvertedBooks (book_id, format, status, converted, counter, conv_ver)
       SELECT id, 1, status, converted, counter, conv_ver FROM Books;
