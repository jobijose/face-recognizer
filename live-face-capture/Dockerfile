
FROM node:22

# Set working directory
WORKDIR /app

# Copy package.json and install dependencies
COPY app/package.json app/package-lock.json ./
RUN npm install

# Copy project files
COPY app/ .
COPY certs/ .

# Build the web app with API endpoint as an environment variable
ARG BACKEND_API_ENDPOINT
ENV BACKEND_API_ENDPOINT=${BACKEND_API_ENDPOINT}
RUN npm run build

RUN npm install -g serve

CMD ["serve", "-s", "build", "--ssl-cert", "client.crt", "--ssl-key", "client.key", "--listen", "3000"]

# Expose port
EXPOSE 3000
