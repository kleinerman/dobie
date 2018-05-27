FROM python:3-alpine

# Install Flask and PyMySQL
RUN \
apk update && apk upgrade && \
pip install --upgrade pip && \
pip install --no-cache-dir Flask && \
pip install --no-cache-dir Flask-HTTPAuth && \
pip install --no-cache-dir PyMySQL && \
apk add --no-cache gcc musl-dev && \
pip install --no-cache-dir gevent && \
apk del musl-dev gcc && \
rm -rf /var/cache/apk/* /root/.cache /tmp/*



# Expose ports:
# - 7979: controller connection port
# - 5000: REST API
EXPOSE 7979 5000
CMD ["python", "-u", "/opt/dobie-server/main.py"]
