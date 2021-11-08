FROM arm64v8/node:lts-alpine

WORKDIR /site


#tzdata is needed to change the timezone
#Once compiled the above, cleaning downloaded packages to reduce the image size
#fomidable and socket.io are modules needed for the node js app
#npm itself is upgraded before installing the above packages

RUN \
apk update && apk upgrade && \
apk add --no-cache tzdata && \
cp /usr/share/zoneinfo/America/Argentina/Cordoba /etc/localtime && \
echo "America/Argentina/Cordoba" > /etc/timezone && \
apk del tzdata && \
rm -rf /var/cache/apk/* /root/.cache /tmp/* && \
npm install --no-fund -g npm && \
npm install --no-fund -g formidable socket.io
