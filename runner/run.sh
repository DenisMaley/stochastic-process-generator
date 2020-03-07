#!/bin/bash

until nc -z ${RABBIT_HOST} ${RABBIT_PORT}; do
    echo "$(date) - waiting for rabbitmq..."
    sleep 1
done

python run.py
echo "$(date) - generating parameter process has started"