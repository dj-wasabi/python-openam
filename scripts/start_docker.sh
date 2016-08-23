#!/usr/bin/env bash


TAG=${1:-13.0.0}

# Start docker OpenAM ${TAG}
docker pull wdijkerman/openam:${TAG}
docker run -d -h openam.example.com --name openam -p 127.0.0.1:8080:8080 wdijkerman/openam:${TAG}

until curl -Is http://127.0.0.1:8080/openam/isAlive.jsp | head -n 1 | grep "200 OK" >/dev/null; do
    sleep 5
done

echo "OpenAM with tag ${TAG} is started and is available"
