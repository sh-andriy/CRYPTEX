#!/bin/bash

# shellcheck disable=SC2046
export $(cat .env | xargs)

gunicorn -w 3 -b 127.0.0.1:5000 'app:create_app()'
