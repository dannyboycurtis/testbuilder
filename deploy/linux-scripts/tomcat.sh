#!/bin/bash

# Required input arguments for script
if [ $# -ne 3 ]
then
    echo 'Usage: <script>.sh <version> <username> <httpport> <installpath> <installershare>'
    exit 0
fi

version=$1
username=$2
httpport=$3
install_path=$4
installer_share=$5

# Check version
case $version in
    "10.3"|"10.3.1")
        tomcat_version = "7.0.22"
        ;;
    "10.4"|"10.4.1")
        tomcat_version = "7.0.65"
        ;;
    "10.5"|"10.5.1")
        tomcat_version = "7.0.72"
        ;;
    "10.6"|"10.6.1")
        tomcat_version = "7.0.82"
        ;;
    *)
        exit
        ;;
esac


# Get Java from shared installer path
# TODO



# Get Tomcat from shared installer path
# TODO



# Configure http/https ports to use
# TODO



# Configure keystore with wildcard certificate and set up https in Tomcat
# TODO



# Enable automatic start of service at reboot and start service
# TODO Copy over arcgistomcat.service file and place in /etc/systemd/system

systemctl enable arcgistomcat.service
systemctl restart arcgistomcat.service
