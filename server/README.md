Dobie infrastructure
====================

Installing Docker
-----------------

**1) Install Docker in your host:**

```
$ sudo pacman -S docker

```

**2) Start and Enable the service:**

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


**3) Storage driver**

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

Creating the docker network
---------------------------

Before creating docker images and container, it's necessary to create a virtual network for the containers

```
$ docker network create --subnet=172.18.0.0/24 --gateway=172.18.0.1 --driver=bridge network_01
```

Running the database server on Docker
-------------------------------------

In order to run Dobie's backend using Docker containers, you should set up a MariaDB database container

**1) Build the image using the Dockerfile**

Before building the image, you must download these files and put them into a `files` directory:

```
$ mkdir -p build/files
$ cd build/files
$ wget https://raw.githubusercontent.com/kleinerman/dobie/master/server/scripts/db_create_drop.sh
$ wget https://raw.githubusercontent.com/kleinerman/dobie/master/server/scripts/db_schema.sql
$ cd ..
$ wget https://raw.githubusercontent.com/kleinerman/dobie/master/server/docker/database/Dockerfile
```

And then, in the `build` directory:

```
$ docker build -t="aryklein/database:0.1" .
```

**2) Create a non-ephemeral storage for the database**

```
$ docker volume create --name database-volume
```

**3) Launch the database container:**

```
$ docker run --net network_01 --ip 172.18.0.2 --name database -v database-volume:/var/lib/mysql -d aryklein/database:0.1
```

**4) Create (if necessary) the database, user and tables:**

```
$ docker exec -it database bash
# root@92d8a1825168:/# bash /tmp/db_create_drop.sh --create
# root@92d8a1825168:/# exit
```

Running the Dobie backend on Docker
-----------------------------------

In this step, we are going to set up the backend process.

Use the Dockerfile (located on this repository) to build the Python container for the backend server.
Put the Dockerfile on a directory and run the following command in the same directory:

```
$ docker build -t="aryklein/backend:0.1" https://raw.githubusercontent.com/jkleinerman/dobie/master/server/docker/backend/Dockerfile
```

**1) Clone the Dobie repository**:

```
$ git clone https://github.com/jkleinerman/dobie.git
```

**2) Launch the Docker container**:

You must map the cloned repository into the container's directory `/opt/app` using Docker volumes. So if the cloned repository is on `/home/USER/dobie` you should run:

```
docker run -d --name backend --net network_01 --ip 172.18.0.3 -p 5000:5000 -p 7979:7979 -v /home/USER/dobie/server/back_end:/opt/app aryklein/backend:0.1 python /opt/app/main.py
```
