#!/bin/bash

TB_PATH="/data/testbuilder/workspace/root/.testbuilder/"



if [ $# -ne 2 ]
then
    echo "Usage script <username> <password>"
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


# Check if testbuilder_settings files exist
declare -a dirs
if [ -e ${TB_PATH}/settings ]
then
    # Add all install and content paths from existing testbuilder_settings file
    dirs= $(cat ${TB_PATH}/settings|grep _dir|cut -d '=' -f 2)
    echo "Install directories found:"
    echo ${dirs}
else
    echo "No settings file detected"
fi
