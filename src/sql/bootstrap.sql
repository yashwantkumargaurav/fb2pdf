-- Bootstapping SQL
-- Defines basic device formats

INSERT INTO Formats (id, title, description) VALUES (1, 'Sony Reader', 'Sony Reader (portrait). Includes: PRS-500,505,700');
INSERT INTO FormatParams (format, name, value) VALUES (1, 'margin','1mm');
INSERT INTO FormatParams (format, name, value) VALUES (1, 'fontsize','12pt');
INSERT INTO FormatParams (format, name, value) VALUES (1, 'papersize','90.6mm,122.4mm');

INSERT INTO Formats (id, title, description) VALUES (2, 'Sony Reader (landscape)', 'Sony Reader (landscape). Includes: PRS-500,505,700');
INSERT INTO FormatParams (format, name, value) VALUES (2, 'margin','1mm');
INSERT INTO FormatParams (format, name, value) VALUES (2, 'fontsize','12pt');
INSERT INTO FormatParams (format, name, value) VALUES (2, 'papersize','122.4mm,90.6mm');

INSERT INTO Formats (id, title, description) VALUES (3, 'ECTACO JetBook', 'ECTACO JetBook (portrait)');
INSERT INTO FormatParams (format, name, value) VALUES (3, 'margin','1mm');
INSERT INTO FormatParams (format, name, value) VALUES (3, 'fontsize','12pt');
INSERT INTO FormatParams (format, name, value) VALUES (3, 'papersize','79mm,100mm');

INSERT INTO Formats (id, title, description) VALUES (4, 'ECTACO JetBook (landscape)', 'ECTACO JetBook (landscape)');
INSERT INTO FormatParams (format, name, value) VALUES (4, 'margin','1mm');
INSERT INTO FormatParams (format, name, value) VALUES (4, 'fontsize','12pt');
INSERT INTO FormatParams (format, name, value) VALUES (4, 'papersize','100mm,79mm');

INSERT INTO Formats (id, title, description) VALUES (5, 'iPhone', 'Apple iPhone (portrait). Includes: iPhone, iPhone3G');
INSERT INTO FormatParams (format, name, value) VALUES (5, 'margin','1mm');
INSERT INTO FormatParams (format, name, value) VALUES (5, 'fontsize','12pt');
INSERT INTO FormatParams (format, name, value) VALUES (5, 'papersize','61mm,115mm');

INSERT INTO Formats (id, title, description) VALUES (6, 'iPhone (landscape)', 'Apple iPhone (landscape). Includes: iPhone, iPhone3G');
INSERT INTO FormatParams (format, name, value) VALUES (6, 'margin','1mm');
INSERT INTO FormatParams (format, name, value) VALUES (6, 'fontsize','12pt');
INSERT INTO FormatParams (format, name, value) VALUES (6, 'papersize','115mm,61mm');

INSERT INTO Formats (id, title, description) VALUES (7, 'Kindle DX', 'Amazon Kindle DX (portrate)');
INSERT INTO FormatParams (format, name, value) VALUES (7, 'margin','1mm');
INSERT INTO FormatParams (format, name, value) VALUES (7, 'fontsize','12pt');
INSERT INTO FormatParams (format, name, value) VALUES (7, 'papersize','132.8mm,194.8mm');

INSERT INTO Formats (id, title, description) VALUES (8, 'Kindle DX (landscape)', 'Amazon Kindle DX (landscape)');
INSERT INTO FormatParams (format, name, value) VALUES (8, 'margin','1mm');
INSERT INTO FormatParams (format, name, value) VALUES (8, 'fontsize','12pt');
INSERT INTO FormatParams (format, name, value) VALUES (8, 'papersize','194.8mm,132.8mm');

INSERT INTO Formats (id, title, description) VALUES (9, 'Kindle 2', 'Amazon Kindle 2 (portrait)');
INSERT INTO FormatParams (format, name, value) VALUES (9, 'margin','1mm');
INSERT INTO FormatParams (format, name, value) VALUES (9, 'fontsize','12pt');
INSERT INTO FormatParams (format, name, value) VALUES (9, 'papersize','90.6mm,122.4mm');

INSERT INTO Formats (id, title, description) VALUES (10, 'Amazon Kindle 2 (landscape)', 'Amazon Kindle 2 (landscape)');
INSERT INTO FormatParams (format, name, value) VALUES (10, 'margin','1mm');
INSERT INTO FormatParams (format, name, value) VALUES (10, 'fontsize','12pt');
INSERT INTO FormatParams (format, name, value) VALUES (10, 'papersize','122.4mm,90.6mm');

