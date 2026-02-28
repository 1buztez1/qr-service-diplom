#!/bin/sh

python insert_db.py
echo "Starting application..."
exec uvicorn main:asgi_app --host 0.0.0.0 --port 5001
