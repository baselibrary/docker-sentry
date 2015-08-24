#!/bin/bash

#enable job control in script
set -e -m

#####   variables  #####
export C_FORCE_ROOT="true" 
# sentry
export SENTRY_CONF="/sentry/sentry.conf.py" 
 
#run in background
if [[ $# -lt 1 ]] || [[ "$1" == "-"* ]]; then
  ##### pre scripts  #####
  echo "========================================================================"
  echo "Prepare: configure the environment:"
  echo "========================================================================"
  sleep 10
  sentry upgrade --noinput
  
  ##### run scripts  #####
  exec forego start "$@" &

  ##### post scripts #####
  
  #bring couchdb to foreground
  fg
else
  exec "$@"
fi
