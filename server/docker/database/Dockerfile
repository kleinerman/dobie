FROM mariadb:latest
LABEL maintainer "Ary Kleinerman"

# MariaDB root password
ENV MYSQL_ROOT_PASSWORD=qwe123qwe

# Listen on all interfaces
RUN sed -i 's/#bind-address/bind-address/' /etc/mysql/my.cnf

