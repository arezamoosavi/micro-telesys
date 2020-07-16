#!/bin/sh


set -o errexit
set -o nounset


uvicorn apis:app --host ${HOST} --port ${PORT} --reload --ws 'auto' \
--loop 'auto' --workers 8

exec "$@"