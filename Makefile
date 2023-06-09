SHELL := /bin/bash
PWD := $(shell pwd)

all:

docker-image:
	docker build -f ./server/Dockerfile -t "server:latest" .
	docker build -f ./result_reducer/Dockerfile -t "result_reducer:latest" .
	docker build -f ./client/Dockerfile -t "client:latest" .
	docker build -f ./station_worker/Dockerfile -t "station_worker:latest" .
	docker build -f ./weather_worker/Dockerfile -t "weather_worker:latest" .
	# Execute this command from time to time to clean up intermediate stages generated 
	# during client build (your hard drive will like this :) ). Don't left uncommented if you 
	# want to avoid rebuilding client image every time the docker-compose-up command 
	# is executed, even when client code has not changed
	# docker rmi `docker images --filter label=intermediateStageToBeDeleted=true -q`
.PHONY: docker-image

docker-compose-up: docker-image
	docker compose -f docker-compose-dev.yaml up -d --build
.PHONY: docker-compose-up

docker-compose-down:
	docker compose -f docker-compose-dev.yaml stop -t 1
	docker compose -f docker-compose-dev.yaml down
.PHONY: docker-compose-down

docker-compose-logs:
	docker compose -f docker-compose-dev.yaml logs -f
.PHONY: docker-compose-logs

docker-network-nuke:
	docker network rm $(docker network ls -q)
.PHONY: docker-network-nuke

docker-network-up:
	docker compose -f docker-compose-infra.yaml up -d --build
.PHONY: docker-network-up

docker-network-down:
	docker compose -f docker-compose-infra.yaml stop -t 1
	docker compose -f docker-compose-infra.yaml down
.PHONY: docker-network-down

docker-network-logs:
	docker compose -f docker-compose-infra.yaml logs -f
.PHONY: docker-network-logs
