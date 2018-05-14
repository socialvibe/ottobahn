#!/bin/sh

gunicorn app:App --log-file=- --reload -b 0.0.0.0:9090
