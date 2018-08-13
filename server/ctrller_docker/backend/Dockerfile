FROM arm32v7/python:3-stretch

# Install Flask and PyMySQL
RUN \
pip install --upgrade pip && \
pip install --no-cache-dir Flask && \
pip install --no-cache-dir Flask-HTTPAuth && \
pip install --no-cache-dir PyMySQL && \
pip install --no-cache-dir gevent



# Expose ports:
# - 7979: controller connection port
# - 5000: REST API
EXPOSE 7979 5000
CMD ["python", "-u", "/opt/dobie-server/main.py"]
