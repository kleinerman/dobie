FROM mariadb:latest
LABEL maintainer "Ary Kleinerman"

# MariaDB root password
ENV MYSQL_ROOT_PASSWORD=qwe123qwe

# Listen on all interfaces
RUN sed -i 's/#bind-address/bind-address/' /etc/mysql/my.cnf

# Copy the deploy database script.
# You should run this script using 'docker exec' command
COPY files/db_create_drop.sh files/db_schema.sql /tmp/
