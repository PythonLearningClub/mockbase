Fake data generator for table-aggregation project + Docker MySQL server to access this data.  
Running it requires Docker Desktop installed and running.  
Running the server:
`make start-mysql`
Server will be acessible on host `127.0.0.1:3306` for user `plc` with no password. Tables you'll need are `db1.table_1` and `db2.table_2`. Results should be stored in table `db3.table_combined`, which needs to be created beforehand.  
Stopping the server:  
`make stop-mysql`  
TODO: right now fakegen fills database with \~1.2M entries instead of \~7M due to mysql server executing startup scripts before fakegen finishes. Look into using makefile + two Dockerfiles to solve this problem. Or [wait-for-it](https://github.com/vishnubob/wait-for-it) script.
