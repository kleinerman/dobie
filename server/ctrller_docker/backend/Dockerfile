FROM arm32v7/python:3-slim

# Flask, Flask-HTTPAuth, requests and gevent are needed for REST API server.
# PyMySQL is needed for database connection.
# pillow is needed to check the person images uploaded format and save them 
# as an images file in the filesystem.

# gcc is needed to compile
# libffi-dev and libssl-dev is needed to compile PyMySQL
# zlib1g-dev and libjpeg-dev is needed to compile pillow
# Once compiled the above, cleaning downloaded packages to reduce the image size

RUN \
apt-get -y update && apt-get -y dist-upgrade && \
apt-get install -y gcc libffi-dev libssl-dev zlib1g-dev libjpeg-dev && \
pip install --upgrade pip && \
pip install --no-cache-dir Flask && \
pip install --no-cache-dir Flask-HTTPAuth && \
pip install --no-cache-dir PyMySQL && \
pip install --no-cache-dir gevent && \
pip install --no-cache-dir requests && \
pip install --no-cache-dir pillow && \
apt-get -y purge libssl-dev libffi-dev gcc zlib1g-dev libjpeg-dev && \
apt-get -y autoremove && \
apt-get -y clean && \
cp /usr/share/zoneinfo/America/Argentina/Cordoba /etc/localtime && \
echo "America/Argentina/Cordoba" > /etc/timezone

