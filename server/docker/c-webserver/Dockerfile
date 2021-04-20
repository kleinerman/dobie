FROM arm64v8/nginx:alpine

RUN \
mkdir /etc/nginx/ssl && \
ln -snf /usr/share/zoneinfo/America/Argentina/Cordoba /etc/localtime

COPY default.conf /etc/nginx/conf.d/
