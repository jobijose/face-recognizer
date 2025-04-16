FROM nginx:alpine

# Remove default Nginx config
RUN rm /etc/nginx/conf.d/default.conf

# Install Certbot for SSL certificate management
RUN apk add --no-cache openssl bash

# Set environment variable for domain
ARG DOMAIN
ARG PROXY_PASS
ENV DOMAIN=$DOMAIN
ENV PROXY_PASS=$PROXY_PASS

RUN mkdir -p /etc/nginx/ssl
COPY ./ssl/client.key /etc/nginx/ssl/client.key
COPY ./ssl/client.crt /etc/nginx/ssl/client.crt

# Copy the Nginx template
COPY nginx.template /etc/nginx/nginx.template
RUN envsubst '$DOMAIN $PROXY_PASS' < /etc/nginx/nginx.template > /etc/nginx/nginx.conf

# Expose custom HTTPS port (change 8443 to your desired port)
EXPOSE 8443

# Copy the entrypoint script
# COPY entrypoint.sh /entrypoint.sh
# RUN chmod +x /entrypoint.sh

# Run entrypoint script
# CMD ["/entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]