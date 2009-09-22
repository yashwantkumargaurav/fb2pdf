-- SQL script to convert db

UPDATE OriginalBooks SET storage_key=REPLACE(storage_key, '.zip', '') WHERE storage_key LIKE '%.zip';

TRUNCATE TitleSearch;
TRUNCATE AuthorSearch;

INSERT INTO TitleSearch (book_id, title) 
       SELECT id, title FROM OriginalBooks;

INSERT INTO AuthorSearch (author) 
       SELECT DISTINCT author FROM OriginalBooks;

DROP TABLE IF EXISTS Books;
