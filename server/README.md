Dobie's infrastructure
======================

Running on Docker (host configuration)
--------------------------------------

In order to run Dobie back\_end server in a Docker container you should follow this procedure:


**Install Docker in your host:**

```
$ sudo pacman -S docker

```

**Start and Enable the service:**


```
$ sudo systemctl start docker.service
$ sudo systemctl enable docker.service
$ sudo docker info
```

By default, the daemon listens on a Unix socket at /var/run/docker.sock for incoming Docker requests.
If a group named docker exists on our system, Docker will apply ownership of the socket to that group.
Hence, any user that belongs to the docker group can run Docker without needing to use the sudo command.
So if you want to be able to run docker as a regular user, add yourself to the docker group:


```
$ sudo gpasswd -a user docker
$ sudo newgrp docker
```


**Storage driver**

Storage driver, a.k.a. graph driver has huge impact on performance. Its job is to store layers of container
images efficiently, that is when several images share a layer, only one layer uses disk space. The default,
most compatible option, devicemapper offers suboptimal performance, which is outright terrible on rotating disks.
Additionally, devicemappper is not recommended in production. As Arch linux ships new kernels, there's no point
using the compatibility option. A good, modern choice is overlay2. To see current storage driver, run:


```
$ docker info | head
```

To set your own choice of storage driver, create a Drop-in snippet and use `-s` option to dockerd:

```
/etc/systemd/system/docker.service.d/override.conf

[Service]
ExecStart=
ExecStart=/usr/bin/dockerd -H fd:// -s overlay2
```

Recall that ExecStart= line is needed to drop inherited ExecStart.


Running on Docker (database server)
-----------------------------------

In order to run Dobie's back-end using Docker containers, you should set up a MariaDB database container

*Build the image using the Dockerfile*

```
$ docker build -t="aryklein/database:0.1" .
```

*Create a non-ephemeral storage for the database*

```
$ docker volume create --name database-volume
```

*Launch the database container:*

```
$ docker run --name database -v database-volume:/var/lib/mysql -d aryklein/database:0.1
```

*Create (if necessary) the database, user and tables:*

```
$ docker exec -it database bash
# root@92d8a1825168:/# /tmp/db_create_drop.sh --create
# root@92d8a1825168:/# exit
```

Running on Docker (back-end server)
-----------------------------------

In this step, we are going to set up the back-end process.


Use the Dockerfile (located on this repository) to build the Python container for the back-end server.
Put the Dockerfile on a directory and run the following command in the same directory:

```
$ docker build -t="aryklein/backend:0.1" .
```

*Clone the Dobie repository*:

```
$ git clone https://USER@github.com/jkleinerman/ConPass.git
```

*Launch the Docker container*:

```
docker run --name backend -p 5000:5000 -p 7979:7979 -v /home/USER/ConPass/server/back_end:/opt/app aryklein/backend:0.1 python /opt/app/main.py
```

