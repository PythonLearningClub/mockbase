LOAD DATA INFILE '/var/lib/mysql-files/insert_a.csv' 
INTO TABLE db1.table_1 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA INFILE '/var/lib/mysql-files/insert_b.csv' 
INTO TABLE db2.table_2 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

