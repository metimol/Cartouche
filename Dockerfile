FROM node:20 AS build
WORKDIR /app
COPY package.json ./
RUN npm ci || npm install
COPY . .
RUN npm run build

FROM nginx:1.25-alpine
COPY --from=build /app/web-build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/frontend.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]