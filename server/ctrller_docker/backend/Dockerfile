FROM arm32v7/python:3-slim
#Install Flask, PyMySQL and gevent(REST Web Server)
#gcc, libffi-dev and libssl-dev is needed to compile PyMySQL
#Once compiled the above, cleaning downloaded packages to reduce the image size

RUN \
apt-get -y update && apt-get -y dist-upgrade && \
apt-get install -y gcc libffi-dev libssl-dev && \
pip install --upgrade pip && \
pip install --no-cache-dir Flask && \
pip install --no-cache-dir Flask-HTTPAuth && \
pip install --no-cache-dir PyMySQL && \
pip install --no-cache-dir gevent && \
apt-get -y purge libssl-dev libffi-dev gcc  && \
apt-get -y autoremove && \
apt-get -y clean && \
cp /usr/share/zoneinfo/America/Argentina/Cordoba /etc/localtime && \
echo "America/Argentina/Cordoba" > /etc/timezone
