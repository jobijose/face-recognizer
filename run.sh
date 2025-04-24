#!/bin/sh

bin/python -m uvicorn app:app --host 0.0.0.0 --port 9090 &
bin/python -m uvicorn app:app --host 0.0.0.0 --port 9443 --ssl-keyfile="resources/ssl/client.key" --ssl-certfile="resources/ssl/client.crt"
