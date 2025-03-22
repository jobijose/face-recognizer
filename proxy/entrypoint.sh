#!/bin/sh

echo "Generating self-signed SSL certificate for $DOMAIN..."
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/nginx/ssl/private.key \
    -out /etc/nginx/ssl/certificate.crt \
     -subj "/C=NL/CN=$DOMAIN"

# Start Nginx
echo "Starting Nginx..."
nginx -g "daemon off;"
