#!/bin/bash


echo "Dobie Server Installation Script"
echo "================================"

function usage {
      echo "usage: $0 [-iclbok -m N -d N]"
      echo "  -i      Run in interactive mode."
      echo "  -c      Install server inside controller."
      echo "  -l      Set log rotate."
      echo "  -b      Configure to start at boot time"
      echo "  -o      Obfuscate the backend source code."
      echo "  -k      Keep git repository."
      echo "  -m N    Store N months of events in DB."
      echo "  -d N    Store N days of DB backups."
      echo "  -h      Display help"
}


function interactive {

      echo "Running in interactive mode.."

      read -p "Are you installing the server in the controller? (y/n): "
      if [[ $REPLY =~ ^[Yy]$ ]]; then
        SRVR_IN_CTRLLR=true
      fi

      read -p "Do you want to set log rotate for server logs? (y/n): "
      if [[ $REPLY =~ ^[Yy]$ ]]; then
        SET_LOG_ROTATE=true
      fi

      read -p "Do you want to start Dobie Server at boot time? (y/n): "
      if [[ $REPLY =~ ^[Yy]$ ]]; then
        START_AT_BOOT=true
      fi

      read -p "Do you want to obfuscate the backend source code? (y/n): "
      if [[ $REPLY =~ ^[Yy]$ ]]; then
        OBFUS_CODE=true
      fi

      read -p "Do you want to keep git repository? (y/n): "
      if [[ $REPLY =~ ^[Yy]$ ]]; then
        KEEP_AS_REPO=true
      fi

      INVALID_ANSWER=true
      while ${INVALID_ANSWER}; do
        read -p "How many months of events do you want to store in Database?: "
        if [[ $REPLY =~ $RE_IS_INT ]]; then
          STORED_MONTHS=$REPLY
          INVALID_ANSWER=false
        else
          echo "Invalid value."
        fi
      done

      INVALID_ANSWER=true
      while $INVALID_ANSWER; do
        read -p "How many days of database backups do you want to store in /var/cache/dobie-db-backups/?: "
        if [[ $REPLY =~ $RE_IS_INT ]]; then
          STORED_DB_BCKPS=$REPLY
          INVALID_ANSWER=false
        else
          echo "Invalid value."
        fi
      done
}


#Initializing default values to variables
SRVR_IN_CTRLLR=false
SET_LOG_ROTATE=false
START_AT_BOOT=false
OBFUS_CODE=false
KEEP_AS_REPO=false
RE_IS_INT='^[0-9]+$'



#if there is no arguments, print usage and exit
if [ $# == 0 ]; then
    usage
    exit 0
fi



while getopts ":iclbokm:d:h" OPT; do
  case $OPT in
    i )
      interactive
      #When running in interactive mode, arguments different from -i are ignored
      break
      ;;

    c )
      echo "Installing server in controller.."
      SRVR_IN_CTRLLR=true
      ;;
    l )
      echo "Setting log roate for server logs.."
      SET_LOG_ROTATE=true
      ;;
    b )
      echo "Configuring to start at boot time.."
      START_AT_BOOT=true
      ;;
    o )
      echo "Obfuscating the source code.."
      OBFUS_CODE=true
      ;;
    k )
      echo "Keeping repository structure.."
      KEEP_AS_REPO=true
      ;;
    m )
      if [[ $OPTARG =~ $RE_IS_INT ]]; then
        STORED_MONTHS=$OPTARG
        echo "Configuring to store $STORED_MONTHS months of events.."
      else
        echo "Invalid number of months set in option -m."
        exit 1
      fi
      ;;
    d )
      if [[ $OPTARG =~ $RE_IS_INT ]]; then
        STORED_DB_BCKPS=$OPTARG
        echo "Configuring to store "$STORED_DB_BCKPS days of database backups..
      else
        echo "Invalid number of days of database backups set in option -d."
        exit 1
      fi
      ;;
    h )
      usage
      exit
      ;;
   \? )
      echo "Invalid option: -$OPTARG"
      usage
      exit 1
      ;;
   : )
      echo "Invalid Option: -$OPTARG requires an argument"
      exit 1
      ;;

  esac
done



##-----------------PERSON'S IMAGE DIRECTORY----------------##

echo "Creating directory to storage person's images.."
sudo mkdir -p /var/lib/dobie-pers-imgs/

##---------------------------------------------------------##





##---------------------------LOGS--------------------------##

echo "Creating directory for Dobie Server Logs.."
sudo mkdir -p /var/log/dobie-s/

if $SET_LOG_ROTATE; then
echo "Configuring log rotation.."
cat > /tmp/dobie-s.logrotate << EOL
/var/log/dobie-s/dobie-s.log
{
    daily
    missingok
    rotate 10
    notifempty
}


/var/log/dobie-s/dobie-purger.log
{
    monthly
    missingok
    rotate 10
    notifempty
}


EOL

sudo cp /tmp/dobie-s.logrotate /etc/logrotate.d/dobie-s
sudo rm /tmp/dobie-s.logrotate
fi


##---------------------------------------------------------##






##--------------------DOCKER CONTAINERS--------------------##

#Change to the directory where the docker-compose.yml file is located and
#save the complete path of the directory in the variable DOCK_COMP_DIR to
#be able to create then the systemd unit to start all the containers
if $SRVR_IN_CTRLLR; then
  cd ../ctrller_docker/
  DOCK_COMP_DIR=$(realpath .)
else
  cd ../docker/
  DOCK_COMP_DIR=$(realpath .)
fi

#Building the containers without starting them
echo "Building Docker containers.."
docker-compose -p dobie up --no-start

##---------------------------------------------------------##






##------------------------SYSTEMD--------------------------##

echo "Setting Dobie Server as Systemd service.."
cat > /tmp/dobie-s.service << EOL
[Unit]
Description=Docker Compose Dobie Containers
After=docker.service network-online.target
Requires=docker.service network-online.target

[Service]
Type=oneshot
RemainAfterExit=yes

ExecStart=/usr/bin/docker-compose -p dobie -f $DOCK_COMP_DIR/docker-compose.yml start
ExecStop=/usr/bin/docker-compose -p dobie -f $DOCK_COMP_DIR/docker-compose.yml stop


[Install]
WantedBy=multi-user.target
EOL
sudo cp /tmp/dobie-s.service /etc/systemd/system/
sudo rm /tmp/dobie-s.service

sudo systemctl daemon-reload


if $START_AT_BOOT; then
  echo "Setting dobie-s.service to start at boot.."
  sudo systemctl enable dobie-s.service
fi


#Starting NOW all the containers using the previously created unit
echo "Starting Dobie server (all the containers).."
sudo systemctl start dobie-s.service

##-------------------------------------------------------##






##----------------------DATABASE-------------------------##


#If there is any previous DB, reset it
echo "Installing a new database and setting initial values to it.."
cd ../scripts/
docker stop backend > /dev/null 2>&1
./db-create-drop.sh -r 
docker start backend > /dev/null 2>&1


##-------------------------------------------------------##





##----------------------PURGE-DB-------------------------##


#Every day at 07:07:07 the purge-old-events.sh is run receiving 
#the amount of months to keep in DB.
#To do this, a systemd timer is created.
cat > /tmp/dobie-purge-db.service << EOL
[Unit]
Description=Purge old events of Dobie DB

[Service]
Type=oneshot
ExecStart=/bin/bash -c 'UNTIL_DATE_TIME=\$\$(date --date "$STORED_MONTHS month ago" +%%Y-%%m-%%d\ %%H:%%M); docker run --name db-purger --rm --network dobie_dobie-net -v $(realpath ../back_end):/opt/dobie-server -v /var/log/dobie-s:/var/log/dobie-s -v /var/lib/dobie-pers-imgs:/var/lib/dobie-pers-imgs dobie_backend python -u /opt/dobie-server/purgeevents.py -d "\$\${UNTIL_DATE_TIME}"'
EOL
#The backslash in $\$\ was used to escape the $ and tell this script not to consider the following as variable.
#The resulting $$, and %% is used to escape $ and % in resulting unit of systemd.
#The "UNTIL_DATE_TIME" variable is filled in the same bash execution of "docker run" execution, to be passed to the "docker run" command.
#Trying to execute $(date..) command inside the docker run command didn't work, since in this case (alphine image),
#"date" command inside the docker, has a minimal options which don't support some arguments used in this one.

sudo cp /tmp/dobie-purge-db.service /etc/systemd/system/
sudo rm /tmp/dobie-purge-db.service 

cat > /tmp/dobie-purge-db.timer << EOL
[Unit]
Description=Weekly purge old events of Dobie DB

[Timer]
OnCalendar=*-*-* 07:07:07

[Install]
WantedBy=timers.target
EOL
sudo cp /tmp/dobie-purge-db.timer /etc/systemd/system/
sudo rm /tmp/dobie-purge-db.timer

sudo systemctl daemon-reload
sudo systemctl enable dobie-purge-db.timer
sudo systemctl start dobie-purge-db.timer


##--------------------------------------------------------##



##-------------SAVE AND RESTORE DB SCRIPTS----------------##


echo "Creating directory for Dobie Server Database Backups.."
sudo mkdir -p /var/cache/dobie-db-backups/

#The following scripts are used to save and restore the DB at any moment.
#They should be executed by the user.
#The script which restores the database, receives the file generated by the
#script which saves the database, as an argument.
#This script stops the backend before restoring the DB to avoid freezing
#in some cases. 
echo "Installing scripts to save and restore Dobie DB.."
cat > /tmp/dobie-save-db << EOL
#!/bin/bash

if [ \$(whoami) != root ]; then
    echo "Please run as root"
    exit 1
fi

. $(realpath db-config)
find /var/cache/dobie-db-backups/ -type f -mtime +$STORED_DB_BCKPS -delete
DB_DOCKER_IP=\$(tr -d '", ' <<< \$(docker inspect database | grep '"IPAddress": "1' | gawk '{print \$2}'))
mysqldump -u \$DB_USER -p\$DB_PASSWD -h \$DB_DOCKER_IP \$DB_DATABASE > /tmp/dobie_sql.dump
DATE_TIME=\$(date +%F_%H%M)
tar czf /var/cache/dobie-db-backups/dobie_db_\$DATE_TIME.tgz -C /tmp/ dobie_sql.dump -C /var/lib/ dobie-pers-imgs/
rm /tmp/dobie_sql.dump

EOL
sudo cp /tmp/dobie-save-db /usr/local/sbin/dobie-save-db
sudo rm /tmp/dobie-save-db
sudo chmod +x /usr/local/sbin/dobie-save-db


cat > /tmp/dobie-restore-db << EOL
#!/bin/bash


if [ \$(whoami) != root ]; then
    echo "Please run as root"
    exit 1
fi

echo "Removing temp files if exist.."
rm -rf /tmp/dobie-pers-imgs/
rm -rf /tmp/dobie_sql.dump

echo "Uncompressing database dump and people images.."
tar xf \$1 -C /tmp/

DB_DOCKER_IP=\$(tr -d '", ' <<< \$(docker inspect database | grep '"IPAddress": "1' | gawk '{print \$2}'))

echo "Stopping Backend.."
docker stop backend

echo "Restoring DB.."
. $(realpath db-config)
mysql -u \$DB_USER -p\$DB_PASSWD -h \$DB_DOCKER_IP \$DB_DATABASE < /tmp/dobie_sql.dump

echo "Restoring people images.."
rm -rf /var/lib/dobie-pers-imgs/
cp -r /tmp/dobie-pers-imgs/ /var/lib/

echo "Removing temp files.."
rm -rf /tmp/dobie-pers-imgs/
rm -rf /tmp/dobie_sql.dump

echo "Starting Backend.."
docker start backend

EOL
sudo cp /tmp/dobie-restore-db /usr/local/sbin/dobie-restore-db
sudo rm /tmp/dobie-restore-db
sudo chmod +x /usr/local/sbin/dobie-restore-db


#Every day at 05:07:07 dobie-save-db is run 
cat > /tmp/dobie-save-db.service << EOL
[Unit]
Description=Dump Dobie DB and remove old dumps.

[Service]
Type=oneshot
ExecStart=/bin/bash -c '/usr/local/sbin/dobie-save-db'
EOL
sudo cp /tmp/dobie-save-db.service /etc/systemd/system/
sudo rm /tmp/dobie-save-db.service

cat > /tmp/dobie-save-db.timer << EOL
[Unit]
Description=Daily dump Dobie DB and remove old dumps.

[Timer]
OnCalendar=*-*-* 05:07:07

[Install]
WantedBy=timers.target
EOL
sudo cp /tmp/dobie-save-db.timer /etc/systemd/system/
sudo rm /tmp/dobie-save-db.timer

sudo systemctl daemon-reload
sudo systemctl enable dobie-save-db.timer
sudo systemctl start dobie-save-db.timer

##------------------------------------------------------------##


##------------------Source Code Obfuscation-------------------##

#Obfuscating the python code in back_end directory
if $OBFUS_CODE; then

  if test -h ../../controller/py_src/msgheaders.py; then
      echo "Replacing msgheader.py symlink in contrller with the real file before obfuscating server files. "
      rm -f ../../controller/py_src/msgheaders.py
      cp ../back_end/msgheaders.py ../../controller/py_src/
  fi

  #Obfuscating the list of files that are in obfuscate.sh script.
  #This is done inside the container.
  docker run --name obfuscater --rm --network dobie_dobie-net -v $(realpath ../back_end):/opt/dobie-server --workdir /opt/dobie-server dobie_backend bash obfuscate.sh

  sudo rm -rf ../back_end/__pycache__/ #Remove if the directory exists from a previous installation
  sudo rm -rf ../back_end/pytransform/ #Remove if the directory exists from a previous installation
  sudo mv ../back_end/dist/* ../back_end/ #Replacing all the plain files with the obfuscated files
  sudo rm -rf ../back_end/dist/ #Remove dist directory

  echo "Restarting the Backend to run with obfuscated source code.."
  docker restart backend
fi


##------------------------------------------------------------##


##----------------Removing Repo Structure----------------------##

if ! $KEEP_AS_REPO; then
    echo "Removing repo structure.."
    sudo rm -rf ../../.git/
    sudo rm -rf ../../.gitignore
    echo "Removing database script files.."
    sudo rm db-config db-create-drop.sh db_schema.sql

    echo "Removing Docs.."
    sudo rm -rf ../../docs/

    if ! $SRVR_IN_CTRLLR; then
        echo "Removing controller source code.."
        sudo rm -rf ../../controller/
    fi


fi

##------------------------------------------------------------##
