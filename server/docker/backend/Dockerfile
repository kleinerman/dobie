FROM python:3-alpine

# Install Flask and PyMySQL and gevent(REST Web Server)
RUN \
apk update && apk upgrade && \
pip install --upgrade pip && \
#musl-dev is needed to compile gevent 
#libffi-dev and openssl-dev is needed to compile PyMySQL
apk add --no-cache gcc musl-dev libffi-dev openssl-dev && \
pip install --no-cache-dir Flask && \
pip install --no-cache-dir Flask-HTTPAuth && \
pip install --no-cache-dir PyMySQL && \
pip install --no-cache-dir gevent && \
#Once compiled the above, cleaning downloaded packages to reduce the image size
apk del openssl-dev libffi-dev musl-dev gcc && \
rm -rf /var/cache/apk/* /root/.cache /tmp/*

# Expose ports:
# - 7979: controller connection port
# - 5000: REST API
EXPOSE 7979 5000
CMD ["python", "-u", "/opt/dobie-server/main.py"]
