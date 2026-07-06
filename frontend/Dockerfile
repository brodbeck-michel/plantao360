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

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget -q --spider http://localhost/nginx-health || exit 1

CMD ["nginx", "-g", "daemon off;"]
