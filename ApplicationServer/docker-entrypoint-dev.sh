#!/bin/sh
set -e

mkdir -p /data/images /data/videos

python /ApplicationServer/utils/create_db.py

exec "$@"