FROM python:3.6.2-alpine3.6

# Install Flask and PyMySQL
RUN \
pip install Flask && \
pip install Flask-HTTPAuth && \
pip install PyMySQL

# Expose ports:
# - 7979: controller connection port
# - 5000: REST API
EXPOSE 7979 5000
