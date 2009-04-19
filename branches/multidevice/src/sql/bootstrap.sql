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
INSERT INTO FormatParams (format, name, value) VALUES (3, 'papersize','79mm,105mm');

INSERT INTO Formats (id, title, description) VALUES (4, 'ECTACO JetBook (landscape)', 'ECTACO JetBook (landscape)');
INSERT INTO FormatParams (format, name, value) VALUES (4, 'margin','1mm');
INSERT INTO FormatParams (format, name, value) VALUES (4, 'fontsize','12pt');
INSERT INTO FormatParams (format, name, value) VALUES (4, 'papersize','105mm,79mm');

INSERT INTO Formats (id, title, description) VALUES (5, 'iPhone', 'Apple iPhone (portrait). Includes: iPhone, iPhone3G');
INSERT INTO FormatParams (format, name, value) VALUES (5, 'margin','1mm');
INSERT INTO FormatParams (format, name, value) VALUES (5, 'fontsize','12pt');
INSERT INTO FormatParams (format, name, value) VALUES (5, 'papersize','61mm,115mm');

INSERT INTO Formats (id, title, description) VALUES (6, 'iPhone (landscape)', 'Apple iPhone (landscape). Includes: iPhone, iPhone3G');
INSERT INTO FormatParams (format, name, value) VALUES (6, 'margin','1mm');
INSERT INTO FormatParams (format, name, value) VALUES (6, 'fontsize','12pt');
INSERT INTO FormatParams (format, name, value) VALUES (6, 'papersize','115mm,61mm');
