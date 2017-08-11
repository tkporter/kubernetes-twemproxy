#!/bin/sh

set -x

# PERIOD=${PERIOD:-300}
YAML=${YAML:-/twemproxy.yaml}
PID_FILE=${PID_FILE:-/twemproxy.pid}
CONFIGURATOR=${CONFIGURATOR:-/create-config.py}

apk add --update curl;
while true; do
  sleep 10;
  python $CONFIGURATOR > /tmp/twemproxy.yaml.update;

  cmp /tmp/twemproxy.yaml.update $YAML;
  if [ $? -ne '0' ]; then
      mv /tmp/twemproxy.yaml.update $YAML;
      kill -s 15 $(cat $PID_FILE);
      /run-twemproxy.sh;
  fi

done
