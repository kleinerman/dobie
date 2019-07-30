FROM nginx:alpine

RUN \
mkdir /etc/nginx/ssl && \
ln -snf /usr/share/zoneinfo/America/Argentina/Cordoba /etc/localtime

COPY default.conf /etc/nginx/conf.d/
COPY server.key /etc/nginx/ssl/
COPY server.crt /etc/nginx/ssl/
COPY dhparam.pem /etc/nginx/ssl/
