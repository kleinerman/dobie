FROM arm64v8/python:3.9-slim
# Flask, Flask-HTTPAuth, requests and gevent are needed for REST API server.
# PyMySQL is needed for database connection.
# pillow is needed to check the person images uploaded format and save them
# as an images file in the filesystem.
# pyarmor is used to run an obfuscate the source code when it is needed.

# gcc is needed to compile
# libffi-dev and libssl-dev is needed to compile PyMySQL
# zlib1g-dev and libjpeg-dev is needed to compile pillow
# Once compiled the above, cleaning downloaded packages to reduce the image size

# As pip is complaining about installing packages as root,
# the backend is run and installed in a virtual environment
# in /dobie-venv.
# Instead of calling the script activate with #source /dobie-vevn/bin/acitvate,
# the /dobie-venv directory was added at the begining of the PATH environment
# variable inside the container. This is the only thing that is needed of the
# activate script.
# Then, when the main.py is executed from the docker-compose.yml, as the
# /dobie-venv directory is first in PATH variable, the python interpreter
# and all the pip packages of the virtual environment will be used.

# apt-get is used instead of apt since apt warns about not using it for scripts.
# DEBIAN_FRONTEND=noniteractive is preceding apt-get install command to avoid
# debconf warns during installation of packages because not having an
# interactive TERM

RUN \
DEBIAN_FRONTEND=noninteractive apt-get -y update && DEBIAN_FRONTEND=noninteractive apt-get -y dist-upgrade && \
DEBIAN_FRONTEND=noninteractive apt-get install -y apt-utils gcc make libffi-dev libssl-dev zlib1g-dev libjpeg-dev && \
cp /usr/share/zoneinfo/America/Argentina/Cordoba /etc/localtime && \
echo "America/Argentina/Cordoba" > /etc/timezone


ENV VENV_DIR=/dobie-venv
RUN python -m venv $VENV_DIR
ENV PATH="$VENV_DIR/bin:$PATH"
RUN \
python -m pip install --upgrade pip && \
python -m pip install --no-cache-dir wheel && \
python -m pip install --no-cache-dir Flask && \
python -m pip install --no-cache-dir Flask-HTTPAuth && \
python -m pip install --no-cache-dir PyMySQL && \
python -m pip install --no-cache-dir gevent && \
python -m pip install --no-cache-dir requests && \
python -m pip install --no-cache-dir pillow && \
python -m pip install --no-cache-dir pyarmor && \
apt-get -y purge libssl-dev libffi-dev gcc zlib1g-dev && \
apt-get -y autoremove && \
apt-get -y clean
