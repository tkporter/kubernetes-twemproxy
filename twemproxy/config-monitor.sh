#!/bin/sh

set -x

PERIOD=${PERIOD:-10}
YAML=${YAML:-/twemproxy.yaml}
PID_FILE=${PID_FILE:-/twemproxy.pid}
CONFIGURATOR=${CONFIGURATOR:-/create-config.py}
TEMP_CONFIG=/tmp/twemproxy.yaml.update
EMPTY=/empty_file

echo "" > $EMPTY

while true; do
  sleep $PERIOD;
  python $CONFIGURATOR > $TEMP_CONFIG;

  cmp $TEMP_CONFIG $EMPTY
  if [ $? -ne '0' ]; then
    cmp $TEMP_CONFIG $YAML;
    if [ $? -ne '0' ]; then
        mv /tmp/twemproxy.yaml.update $YAML;
        if [ -f $PID_FILE ]; then
          PID=`cat $PID_FILE`
          rm -f $PID_FILE;
          kill -s 15 $PID;
        fi
    fi

  fi

done
