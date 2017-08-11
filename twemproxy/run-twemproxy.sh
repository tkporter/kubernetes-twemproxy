#!/bin/sh

/config-monitor.sh /create-config.py &

while [ ! -f /twemproxy.yaml ]; do
    echo 'Waiting for twemproxy.yaml...'
    sleep 1
done

EXIT_CODE=143
while [ $EXIT_CODE = 143 ]; do
    echo 'Starting twemproxy'
    nutcracker -p /twemproxy.pid -c /twemproxy.yaml -v 7 -s 22222
    EXIT_CODE=$?
done

exit $EXIT_CODE
