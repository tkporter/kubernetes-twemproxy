#!/bin/sh

set -x

PERIOD=${PERIOD:-5}
YAML=${YAML:-/twemproxy.yaml}
PID_FILE=${PID_FILE:-/twemproxy.pid}
CONFIGURATOR=${CONFIGURATOR:-/create-config.py}

apk add --update curl;
while true; do
  sleep $PERIOD;
  python $CONFIGURATOR > /tmp/twemproxy.yaml.update;

  cmp /tmp/twemproxy.yaml.update $YAML;
  if [ $? -ne '0' ]; then
      mv /tmp/twemproxy.yaml.update $YAML;
      if [ -f $PID_FILE ]; then
        kill -s 15 $(cat $PID_FILE);
      fi
      /run-twemproxy.sh;
  fi

done
