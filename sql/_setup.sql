CREATE DATABASE IF NOT EXISTS db1;
USE db1;
DROP TABLE IF EXISTS table_1;
CREATE TABLE table_1 (
    merchant_id SMALLINT,
    message_filter_id INT,
    sent_date DATE,
    total_cnt SMALLINT,
    success_cnt SMALLINT,
    problematic_cnt SMALLINT,
    mtm_problematic_cnt SMALLINT,
    nbo_cnt SMALLINT,
    non_usd_count SMALLINT,
    PRIMARY KEY(message_filter_id, sent_date)
);
CREATE DATABASE IF NOT EXISTS db2;
USE db2;
DROP TABLE IF EXISTS table_2;
CREATE TABLE table_2 (
    merchantid SMALLINT, 
    filterid INT, 
    orderdate DATE, 
    ordercount SMALLINT,
    PRIMARY KEY(filterid, orderdate)
);
CREATE DATABASE IF NOT EXISTS db3;
