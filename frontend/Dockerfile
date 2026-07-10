FROM node:20-alpine AS builder

ARG VITE_MVP_MODE=true
ENV VITE_MVP_MODE=$VITE_MVP_MODE

WORKDIR /app

COPY frontend/package.json ./
RUN npm install

COPY frontend/ .
RUN npx vite build

FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html
COPY docker/nginx/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

# Use 127.0.0.1 (not "localhost") — inside the container "localhost" may resolve
# to ::1 (IPv6) first, but nginx only listens on IPv4 (listen 80), causing the
# healthcheck to fail with "connection refused" even though the site is healthy.
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget -q --spider http://127.0.0.1/nginx-health || exit 1

CMD ["nginx", "-g", "daemon off;"]
