#!/bin/bash


echo "Dobie Server Uninstallation Script"
echo "=================================="

function usage {
      echo "usage: $0 [-icbph]"
      echo "  -i      Run in interactive mode."
      echo "  -c      Remove containers."
      echo "  -b      Remove database backups."
      echo "  -p      Remove person's images"
      echo "  -h      Display help"
}


function interactive {

      echo "Running in interactive mode.."

      read -p "Are you sure to uninstall Dobie Server? (y/n): "
        if ! [[ $REPLY =~ ^[Yy]$ ]]; then
          exit 0
        fi

      read -p "Do you want to remove all Docker containers, volumes and networks? (y/n): "
      if [[ $REPLY =~ ^[Yy]$ ]]; then
        REM_CONTS=true
      fi

      read -p "Do you want to remove Database Backcups (/var/cache/dobie-db-backups/)? (y/n): "
      if [[ $REPLY =~ ^[Yy]$ ]]; then
        REM_DB_BCKPS=true
      fi

      read -p "Do you want to remove person's images files (/var/lib/dobie-pers-imgs/)? (y/n): "
      if [[ $REPLY =~ ^[Yy]$ ]]; then
        REM_PERS_IMGS=true
      fi


}


#Initializing default values to variables
REM_CONTS=false
REM_DB_BCKPS=false
REM_PERS_IMGS=false
RE_IS_INT='^[0-9]+$'


#if there is no arguments, print usage and exit
if [ $# == 0 ]; then
  usage
  exit 0
fi



while getopts ":icbph" OPT; do
  case $OPT in
    i )
      interactive
      #When running in interactive mode, arguments different from -i are ignored
      break
      ;;

    c )
      echo "Setting to remove Docker containers, volumes and networks.."
      REM_CONTS=true
      ;;
    b )
      echo "Setting to remove Database Backcups.."
      REM_DB_BCKPS=true
      ;;
    p )
      echo "Setting to remove person's images files.."
      REM_PERS_IMGS=true
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



echo "Removing Dobie Server Logs directory.."
sudo rm -rf /var/log/dobie-s/

echo "Removing Log rotation file.."
sudo rm /etc/logrotate.d/dobie-s


if $REM_DB_BCKPS; then
  echo "Removing Database Backcups.."
  sudo rm -rf /var/cache/dobie-db-backups
fi

if $REM_PERS_IMGS; then
  echo "Removing person's images files.."  
  sudo rm -rf /var/lib/dobie-pers-imgs
fi


echo "Stoping all systemd units.."
sudo systemctl stop dobie-purge-db.timer
sudo systemctl stop dobie-save-db.timer
sudo systemctl stop dobie-s.service

echo "Disabling and removing systemd units.."
sudo systemctl disable dobie-purge-db.timer
sudo systemctl disable dobie-save-db.timer
sudo systemctl disable dobie-s.service
sudo rm /etc/systemd/system/dobie-purge-db.timer
sudo rm /etc/systemd/system/dobie-purge-db.service
sudo rm /etc/systemd/system/dobie-save-db.timer
sudo rm /etc/systemd/system/dobie-save-db.service
sudo rm /etc/systemd/system/dobie-s.service
sudo systemctl daemon-reload

echo "Removing scripts to save and restore DB.."
sudo rm /usr/local/sbin/dobie-save-db
sudo rm /usr/local/sbin/dobie-restore-db

if $REM_CONTS; then
  echo "Removing Docker containers, volumes and networks.."
  sudo docker rm $(docker ps -a -q)
  sudo docker rmi -f $(docker images -q)
  sudo docker volume rm dobie_database-volume
  sudo docker network rm dobie_dobie-net
  sudo docker builder prune -a -f
fi


