FROM node:20 AS build
WORKDIR /app
COPY package.json ./
RUN npm ci || npm install
COPY . .
# Создаем index.html в корне проекта для Vite
RUN mkdir -p public && cp src/web/index.html public/index.html
# Исправляем путь к скрипту в index.html
RUN sed -i 's|src="./index.tsx"|src="./src/web/index.tsx"|g' public/index.html
RUN npm run build

FROM nginx:1.25-alpine
COPY --from=build /app/web-build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
