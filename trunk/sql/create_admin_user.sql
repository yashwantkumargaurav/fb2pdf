-- Creates user 'fb2pdfadmin' and grants him appropriate permissions
--
-- must be executed as mysql administrator
-- WARNING: created user have full control over your mysql instance!
-- Practivally user 'counseloradmin' becomes new administrator.
-- Unfortunately it is required to be able to create FB2PDF database and
-- users. Use with caution!

GRANT ALL ON *.* TO fb2pdfadmin@'localhost.localdomain' IDENTIFIED BY '8SLpnin7' WITH GRANT OPTION ;
GRANT ALL ON *.* TO fb2pdfadmin@'localhost' IDENTIFIED BY '8SLpnin7' WITH GRANT OPTION ;
GRANT ALL ON *.* TO fb2pdfadmin@'%' IDENTIFIED BY '8SLpnin7' WITH GRANT OPTION ;
