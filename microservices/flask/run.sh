#!/bin/sh


set -o errexit
set -o nounset

# run gunicorn
gunicorn apis:app -b ${HOST}:${PORT} --access-logfile '-'

exec "$@"