FROM python:3-alpine

# Install Flask and PyMySQL and gevent(REST Web Server)

#musl-dev is needed to compile gevent 
#libffi-dev and openssl-dev is needed to compile PyMySQL
#tzdata is needed to change the timezone
#Once compiled the above, cleaning downloaded packages to reduce the image size

RUN \
apk update && apk upgrade && \
pip install --upgrade pip && \
apk add --no-cache gcc musl-dev libffi-dev openssl-dev tzdata && \
pip install --no-cache-dir Flask && \
pip install --no-cache-dir Flask-HTTPAuth && \
pip install --no-cache-dir PyMySQL && \
pip install --no-cache-dir gevent && \
pip install --no-cache-dir requests && \
cp /usr/share/zoneinfo/America/Argentina/Cordoba /etc/localtime && \
echo "America/Argentina/Cordoba" > /etc/timezone && \
apk del openssl-dev libffi-dev musl-dev gcc tzdata && \
rm -rf /var/cache/apk/* /root/.cache /tmp/*

