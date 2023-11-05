#!/bin/sh

if ! test -d ./db; then
    mkdir ./db
fi

if ! test -f ./db/database.db; then
  touch db/database.db
fi

chmod a+rwX ./db

docker build -t wagerwhales .
docker run --name wagerwhales \
            -v ./db:/var/db \
            -v ./frontend/dist:/home/user/frontend/dist \
            --rm \
            -p 127.0.0.1:8080:80 \
            -e HOST=$1 \
            wagerwhales