#!/usr/bin/env bash

CONTAINER_NAME=$(docker ps -a | awk '{print $NF}' | grep ^openam)

if [[ -n ${CONTAINER_NAME} ]]
    then    docker kill ${CONTAINER_NAME}
            docker rm ${CONTAINER_NAME}
fi
