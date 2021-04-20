FROM arm64v8/mariadb:latest
LABEL maintainer "Ary Kleinerman"

# MariaDB root password
ENV MYSQL_ROOT_PASSWORD=qwe123qwe

# Listen on all interfaces and set timezone to GMT-3
RUN sed -i 's/#bind-address/bind-address/' /etc/mysql/my.cnf && ln -snf /usr/share/zoneinfo/America/Argentina/Cordoba /etc/localtime

