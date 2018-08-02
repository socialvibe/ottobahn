#!/bin/sh

#./ngrok http 9090

while true; do
#	gunicorn app:App --log-file=- --reload -b 0.0.0.0:9090 &
#	sleep $(( 30 * 60 ));
#	kill -9 `ps aux | grep gunicorn | grep 9090 | awk '{ print $2 }'`;

	date;
	gunicorn app:App --log-file=- --reload -b 0.0.0.0:9090 2>&1 |  grep -io -m 1 "error" | head -1
	sleep 1;
done
