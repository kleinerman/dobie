FROM python:3-alpine

# Flask, Flask-HTTPAuth, requests and gevent are needed for REST API server.
# PyMySQL is needed for database connection.
# pillow is needed to check the person images uploaded format and save them 
# as an images file in the filesystem.

# musl-dev is needed to compile gevent 
# libffi-dev and openssl-dev is needed to compile PyMySQL
# tzdata is needed to change the timezone
# zlib-dev and jpeg-dev is needed to compile pillow
# Once compiled the above, cleaning downloaded packages to reduce the image size

RUN \
apk update && apk upgrade && \
pip install --upgrade pip && \
apk add --no-cache gcc musl-dev libffi-dev openssl-dev tzdata zlib-dev jpeg-dev && \
pip install --no-cache-dir Flask && \
pip install --no-cache-dir Flask-HTTPAuth && \
pip install --no-cache-dir PyMySQL && \
pip install --no-cache-dir gevent && \
pip install --no-cache-dir requests && \
pip install --no-cache-dir pillow && \
cp /usr/share/zoneinfo/America/Argentina/Cordoba /etc/localtime && \
echo "America/Argentina/Cordoba" > /etc/timezone && \
apk del openssl-dev libffi-dev musl-dev gcc tzdata zlib-dev && \
rm -rf /var/cache/apk/* /root/.cache /tmp/*

