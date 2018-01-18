FROM python:3-alpine

# Install Flask and PyMySQL
RUN \
pip install Flask && \
pip install Flask-HTTPAuth && \
pip install PyMySQL

# Expose ports:
# - 7979: controller connection port
# - 5000: REST API
EXPOSE 7979 5000
CMD ["python", "-u", "/opt/dobie-server/main.py"]
