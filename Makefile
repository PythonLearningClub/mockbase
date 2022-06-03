build-faker:
	docker build -t fakegen/fakegen:latest .

run-faker:
	docker run --rm --name=faker -v=mysql:/fakegen/sql -v=fakegen-volume:/fakegen/insert -d fakegen/fakegen:latest

check-volume:
	docker run --rm -i -v=mysql:/tmp/myvolume busybox find /tmp/myvolume

get-logs-faker:
	docker logs faker  2>&1

get-mysql-pwd:
	docker logs mysql 2>&1 | grep GENERATED

prune:
	docker container prune -f

connect-mysql:
	docker exec -it mysql /bin/bash

start-mysql:
	docker-compose up

stop-mysql:
	docker-compose down -v
