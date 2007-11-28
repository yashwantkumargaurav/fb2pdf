ALTER TABLE Books ADD COLUMN isbn VARCHAR(16) NULL AFTER title;
ALTER TABLE Books ADD COLUMN converted DATETIME NULL AFTER status;
ALTER TABLE Books ADD COLUMN counter INT DEFAULT 0 NOT NULL AFTER converted;

ALTER TABLE Books ADD INDEX converted_idx (converted);
ALTER TABLE Books ADD INDEX counter_idx (counter);

ALTER TABLE Books MODIFY storage_key VARCHAR(64) NOT NULL;
