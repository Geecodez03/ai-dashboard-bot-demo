#!/usr/bin/env bash
set -e
gunicorn -w 2 -k gthread -t 120 -b 0.0.0.0:${PORT:-5000} backend.wsgi:app
