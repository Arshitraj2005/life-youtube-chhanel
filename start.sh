#!/bin/bash
gunicorn main:app --bind 0.0.0.0:$PORT &

# Wait for Flask to initialize
sleep 5

# Start your YouTube stream
python3 stream.py
