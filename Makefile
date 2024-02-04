PROJECT=master

IMAGE_BASE=job-assistant

docker-build:
	IMAGE_BASE=$(IMAGE_BASE) ./scripts/docker/build.sh

docker-start:
	@ docker-compose -p $(PROJECT) up -d --build

docker-stop:
	@ docker-compose -p $(PROJECT) rm -fsv