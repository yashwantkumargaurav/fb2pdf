-- Creates FB2PDF database
-- must be executed as user 'fb2pdfadmin'

CREATE DATABASE FB2PDF DEFAULT CHARACTER SET utf8;
GRANT ALL PRIVILEGES ON FB2PDF.* TO fb2pdf@'localhost.localdomain' IDENTIFIED BY 'lP51Sedr';
GRANT ALL PRIVILEGES ON FB2PDF.* TO fb2pdf@'localhost' IDENTIFIED BY 'lP51Sedr';
GRANT ALL PRIVILEGES ON FB2PDF.* TO fb2pdf@'%' IDENTIFIED BY 'lP51Sedr9';

GRANT LOCK TABLES ON FB2PDF.* TO fb2pdf@'localhost.localdomain' IDENTIFIED BY 'lP51Sedr';
GRANT LOCK TABLES ON FB2PDF.* TO fb2pdf@'localhost' IDENTIFIED BY 'lP51Sedr';
GRANT LOCK TABLES ON FB2PDF.* TO fb2pdf@'%' IDENTIFIED BY 'lP51Sedr';

