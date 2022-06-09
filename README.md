Fake data generator for table-aggregation project + Docker MySQL server to access this data.  
Running it requires Docker Desktop and docker-compose (version >= 1.2.9) installed and running.  
Running the server:   
`make start-mysql`  
Server will be acessible on host `127.0.0.1:3306` for user `plc` with no password. Tables you'll need are `db1.table_1` and `db2.table_2`. Results should be stored in table `db3.table_combined`, which needs to be created beforehand.  
Stopping the server:  
`make stop-mysql`   
