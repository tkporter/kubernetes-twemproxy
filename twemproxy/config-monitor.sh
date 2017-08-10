#!/bin/sh

set -x

apk add --update curl;
while true; do
  sleep 5;
  python $1;
done
