FROM arm32v7/node:carbon-slim

WORKDIR /site

RUN \
cp /usr/share/zoneinfo/America/Argentina/Cordoba /etc/localtime && \
echo "America/Argentina/Cordoba" > /etc/timezone && \
npm install -g formidable socket.io

