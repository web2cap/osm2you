FROM node:20-bullseye-slim AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
CMD cp -r build result_build