#!/bin/bash
# This script prepares a node for a fresh installation
# It will uninstall all arcgis software (and tomcat) as well as recreate
# the specified user and add entrie to limits.conf for the user

# Required input arguments for script
if [ $# -ne 2 ]
then
    echo 'Usage: <script>.sh <username> <password>'
    exit 0
fi

username=$1
password=$2


# Check if service scripts were set up for ArcGIS services
if [ -e /etc/systemd/system/arcgis* ]
then
    # Stop arcgis services
    systemctl stop arcgisserver.service
    systemctl stop arcgisportal.service
    systemctl stop arcgisdatastore.service
    systemctl stop arcgistomcat.service

    # Disable arcgis services
    systemctl disable arcgisserver.service
    systemctl disable arcgisportal.service
    systemctl disable arcgisdatastore.service
    systemctl disable arcgistomcat.service

    # Remove service files from /etc/systemd/system
    rm -f /etc/systemd/system/arcgis*
fi


# Check if .testbuilder_properties files exist
declare -a dirs
if [ -e /home/*/.testbuilder/properties ]
then
    # Add all install and content paths from existing .testbuilder_properties file
    dirs= $(cat /root/.testbuilder/properties|grep _dir|cut -d '=' -f 2)
fi


# Delete all testbuilder_properties files
rm -f /home/*/.testbuilder/properties


# Check if .ESRI.properties files exist
if [ -e /home/*/.ESRI.properties* ]
then
    # Add all install paths from existing .ESRI.properties files
    for propfile in $(ls -a /home/*/.ESRI.properties*)
    do
        dirs=( "${dirs[@]}" "$( cat ${propfile}|grep INSTALL_DIR|cut -d '=' -f 2)" )
    done
fi


# Delete all .ESRI.properties files
rm -Rf /home/*/.ESRI.properties*


# Delete all directories found in properties file
for dir in ${dirs}
do
    rm -Rf dir
done


# Check is username exists, if it does, delete it (and home dir) then add again
if [ $( grep -c ^${username} /etc/passwd) == 1 ]
then
    userdel ${username}
    rm -Rf /home/${username}
fi


# Add username, set password and create home directory
useradd ${username} -p ${password} -m


# Remove and add entries to /etc/security/limits.conf
sed -i '/'${username}'/d' /etc/security/limits.conf
echo -e "${username}\t\t-\tnofile\t\t65535" >> /etc/security/limits.conf
echo -e "${username}\t\t-\tnproc\t\t25059" >> /etc/security/limits.conf

exit 0