#!/usr/bin/bash

## Vars

ARGS="ush"
UFLAG=0
SFLAG=0
NETWORK_CONFIGURED=0
PACMAN=/usr/bin/pacman
USERADD=/usr/bin/useradd
USERMOD=/usr/bin/usermod
PACKAGES="sudo bash-completion python vim base-devel git"
TIME_ZONE="America/Argentina/Cordoba"
IFACE=eth0
COLOR_ORANGE="\033[0;33m"
NO_COLOR="\033[0m"

##


# Validate the user IP address
function validate_ip {
    local IPADDRESS=$1
    local VALID_IP=1

    if [[ $IPADDRESS =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
        # Save the original internal field separator and change it by .
        ORIGINAL_IFS=$IFS
        IFS="."
        
        # Split the address and save it on a list
        IPADDRESS=( $IPADDRESS )
        
        # Go back to the original internal field separator
        IFS=$ORIGINAL_IFS
        
        # Check that each octet is less than 255
        [[ ${IPADDRESS[0]} -le 255 && ${IPADDRESS[1]} -le 255 && ${IPADDRESS[2]} -le 255 \
           && ${IPADDRESS[3]} -le 255 ]]
        
        VALID_IP=$?
    fi

    if [[ $VALID_IP -eq 1 ]]; then
        echo "Error: It's not a valid IP address"
        exit 1
    fi

}

function set_network {
    printf "IP Address: "; read IPADDRESS
    validate_ip $IPADDRESS 

    printf "Netmask (CIDR format): "; read NETMASK
    if ! [[ $NETMASK -gt 0 && $NETMASK -le 32 ]]; then
        echo "Error: wrong netmask"
        exit 1
    fi

    printf "Gateway: "; read GATEWAY
    validate_ip $GATEWAY

    printf "DNS server: "; read DNS
    validate_ip $DNS

}


#### main ####

# Check root permissions
if [ "$EUID" -ne 0 ]; then echo "Please run as root" && exit 1; fi


# User arguments
while getopts $ARGS OPTION; do
    case $OPTION in
        u)  UFLAG=1
            printf "Users to add (separated by spaces): "; read USERS
            USERS=( $USERS )
            ;;

        s)  SFLAG=1
            set_network
            ;;

        h)  echo "Usage: `basename $0` [-u] [-s]"
            printf "${COLOR_ORANGE}-u${NO_COLOR}, Create users\n"
            printf "${COLOR_ORANGE}-s${NO_COLOR}, Set static IP address\n"
            exit 0;
            ;;

        ?)  printf "Error: Invalid argument.\n"
            exit 1
            ;;
    esac
done


# Determine if you are logged in via SSH or on the local machine
# If you are not logged in via SSH and SFLAG is set to 1,
# start with network configuration.
if [[ ! $(who am i) =~ \([0-9\.]+\)$ && $SFLAG -eq 1 ]] ; then
    printf "[Match]\nName=$IFACE\n\n[Network]\nAddress=$IPADDRESS/$NETMASK\nGateway=$GATEWAY\nDNS=$DNS\n" > /etc/systemd/network/eth0.network
    systemctl restart systemd-networkd.service
    NETWORK_CONFIGURED=1
fi


##
# Update package list and upgrade all packages afterwards. Then install packages
# that are not installed on the system.

# Get a list with all not installed packages
for PACKAGE in $PACKAGES; do
    if ! $PACMAN -Q $PACKAGE 1> /dev/null 2>&1; then
        NEW_PACKAGES+="$PACKAGE "
    fi
done

# Check Internet connection before update, upgrade and install process
if `ping -c3 www.google.com > /dev/null`; then
    $PACMAN --noconfirm -Syu
    $PACMAN --noconfirm -S $NEW_PACKAGES
else
    echo "Error: there is not Internet connection. Aborting..."
    exit 1
fi


## Some improvements
# Colored prompt for root and other users
sed -i "s/PS1=.*/PS1='\\\[\\\e[1;32m\\\][\\\u@\\\h \\\W]\\\$\\\[\\\e[0m\\\] '/" /etc/skel/.bashrc
sed -i "s/PS1=.*/PS1='\\\[\\\e[1;31m\\\][\\\u@\\\h \\\W]\\\$\\\[\\\e[0m\\\] '/" /etc/bash.bashrc

# Some tuning for VIM 
rm /usr/bin/vi && ln -s /usr/bin/vim /usr/bin/vi
cp /usr/share/vim/vim74/vimrc_example.vim /etc/vimrc
echo "set background=dark" >> /etc/vimrc

# ls and grep colored for all users
dircolors -p > /etc/DIR_COLORS
echo "[ -r /etc/DIR_COLORS ] && eval \`dircolors -b /etc/DIR_COLORS\`" >> /etc/bash.bashrc
echo "alias ls='ls --color=auto'" | tee -a /etc/bash.bashrc /etc/skel/.bashrc 1> /dev/null
echo "alias grep='grep --color=auto'" | tee -a /etc/bash.bashrc /etc/skel/.bashrc 1> /dev/null

# Create users if "-u" option is used
if [[ $UFLAG -eq 1  ]]; then
    echo "========================================="
    echo "#########################################"
    echo ""
    for USER in ${USERS[@]}; do
        PASSWORD=`dd if=/dev/urandom bs=1 count=6 2>/dev/null | base64`
        echo "Password for user \"$USER\": $PASSWORD"
        HASHEDPASS=`python -c "import crypt; print(crypt.crypt('$PASSWORD', crypt.METHOD_SHA512));"`
        useradd -m -s /bin/bash $USER
        usermod -p $HASHEDPASS $USER
        chage -d 0 $USER
        gpasswd -a $USER wheel
    done
    echo ""
    echo "========================================="
    echo "#########################################"

fi


##
# Uncomment to allow members of group wheel to execute any command
sed -i 's/# \(%wheel ALL=(ALL) NOPASSWD: ALL\)/\1/' /etc/sudoers

##
# Set timezone
timedatectl set-timezone $TIME_ZONE

## Set network parameters
#
if [[ $UFLAG -eq 1 && $NETWORK_CONFIGURED -eq 0  ]]; then
    # Modify the network file configuration and restart the service unit
    printf "[Match]\nName=$IFACE\n\n[Network]\nAddress=$IPADDRESS/$NETMASK\nGateway=$GATEWAY\nDNS=$DNS\n" > /etc/systemd/network/eth0.network
    echo "Deploy finished. The IP address has changed. Connect again with this IP address: $IPADDRESS"
    echo "See you again"
    systemctl restart systemd-networkd.service
fi

