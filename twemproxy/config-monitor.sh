#!/bin/sh

set -x

PERIOD=${PERIOD:-10}
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
        PID=`cat $PID_FILE`
        rm -f $PID_FILE;
        kill -s 15 $PID;
      fi
  fi

done
