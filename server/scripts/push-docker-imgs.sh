#!/bin/bash


function usage {
      echo "usage: $0 [-c -t <tag> ]"
      echo "  -c        Push images that run in controller."
      echo "  -t <tag>  Tag of the image."
      echo "  -h        Display help"
}




#if there is no arguments, print usage and exit
if [ $# == 0 ]; then
    usage
    exit 0
fi


#Initializing variables
SRVR_IN_CTRLLR=false
IMAGE_NAMES=(backend database webserver php nodejs)

while getopts ":ct:h" OPT; do
  case $OPT in
    c )
      SRVR_IN_CTRLLR=true
      ;;
    t )
      IMG_TAG=$OPTARG
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



if $SRVR_IN_CTRLLR; then
    IMG_PRFX=c-
else
    IMG_PRFX=s-
fi



echo "Login in Docker Hub.."
docker login --username=dobie

for IMAGE in ${IMAGE_NAMES[@]}; do
    docker tag dobie/${IMG_PRFX}${IMAGE}:latest dobie/${IMG_PRFX}${IMAGE}:${IMG_TAG}
    docker push dobie/${IMG_PRFX}${IMAGE}:${IMG_TAG}
    docker push dobie/${IMG_PRFX}${IMAGE}:latest
done

echo "Logout from Docker Hub.."
docker logout


