FROM node:lts-alpine

RUN npm install -g http-server

WORKDIR /app

COPY ./frontend/package*.json ./

RUN npm install

COPY ./frontend .

RUN npm run build

EXPOSE 8080

CMD [ "npm", "run", "serve" ]
