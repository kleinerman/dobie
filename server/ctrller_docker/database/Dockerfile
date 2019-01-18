FROM yobasystems/alpine-mariadb:arm32v7
LABEL maintainer "Ary Kleinerman"

# MariaDB root password
ENV MYSQL_ROOT_PASSWORD=qwe123qwe

RUN \
#Changing timezone
apk update && apk upgrade && \
apk add --no-cache tzdata && \
cp /usr/share/zoneinfo/America/Argentina/Cordoba /etc/localtime && \
echo "America/Argentina/Cordoba" > /etc/timezone && \
apk del tzdata && \
rm -rf /var/cache/apk/* /root/.cache /tmp/* && \
# Make the engine listen on all interfaces
sed -i 's/#bind-address/bind-address/' /etc/mysql/my.cnf

