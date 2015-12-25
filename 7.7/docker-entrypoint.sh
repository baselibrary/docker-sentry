#!/bin/bash

#enable job control in script
set -e -m

#####   variables  #####
export C_FORCE_ROOT="true" 

#run command in background
if [[ $# -lt 1 ]] || [[ "$1" == "-"* ]]; then
  ##### pre scripts  #####
  echo "========================================================================"
  echo "initialize:"
  echo "========================================================================"
  mkdir -p $SENTRY_DATA_DIR && sentry upgrade --noinput
  
  ##### run scripts  #####
  echo "========================================================================"
  echo "startup:"
  echo "========================================================================"
  exec goreman start "$@" &

  ##### post scripts #####
  echo "========================================================================"
  echo "configure:"
  echo "========================================================================"
  
  #bring command to foreground
  fg
else
  exec "$@"
fi
