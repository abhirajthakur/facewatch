FROM node:24-alpine AS builder

WORKDIR /app

ARG VITE_WS_URL
ENV VITE_WS_URL=$VITE_WS_URL

COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build

FROM nginx:stable-alpine

COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
