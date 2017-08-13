#!/bin/sh
set -e

mkdir -p /data/images /data/videos

python /ApplicationServer/utils/create_db.py

echo 'Starting Application'
exec gunicorn app --bind=0.0.0.0:8000 --preload "$@"
exec "$@"