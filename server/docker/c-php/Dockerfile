FROM arm64v8/php:8-fpm-alpine


#tzdata is needed to change the timezone
#Once compiled the above, cleaning downloaded packages to reduce the image size
#fomidable and socket.io are modules needed for the node js app

RUN \
apk update && apk upgrade && \
apk add --no-cache tzdata && \
cp /usr/share/zoneinfo/America/Argentina/Cordoba /etc/localtime && \
echo "America/Argentina/Cordoba" > /etc/timezone && \
apk del tzdata && \
rm -rf /var/cache/apk/* /root/.cache /tmp/*
