FROM php:7-fpm-alpine


#tzdata is needed to change the timezone
#Once compiled the above, cleaning downloaded packages to reduce the image size

RUN \
apk update && apk upgrade && \
apk add --no-cache tzdata && \
cp /usr/share/zoneinfo/America/Argentina/Cordoba /etc/localtime && \
echo "America/Argentina/Cordoba" > /etc/timezone && \
apk del tzdata && \
rm -rf /var/cache/apk/* /root/.cache /tmp/*
