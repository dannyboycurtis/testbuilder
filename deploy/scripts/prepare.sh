#!/bin/bash

# Required input arguments for script
if [ $# -lt 1 ]; then
    echo 'Usage: prepare.sh <version> -s /path/to/share -u username -p password]'
    exit 1
fi

# Check for valid version
if [ $(echo "$3"|cut -d '.' -f 1) -ne "10" ] || [ $(echo "$1"|cut -d '.' -f 2) -lt 3 ]; then
    echo "Supported versions: 10.3 - 10.6.1"
    exit 1
else
    version="$1"
fi

# Check for options
while [ $# -gt 0 ]
do
    case $1 in
        -s)
            # Exit if path specified is invalid
            if ! [ -e "$2" ]; then
                echo "$2 is either invalid or inaccessible"
                exit 1
            fi
            share_path="$2"
            ;;
        -p)
            # Set password
            password="$2"
            ;;
        -u)
            # If user exists, clear password
            if [ $( grep -c ^"$2" /etc/passwd) == 1 ]; then
                passwd -d "$2" >> /dev/null
            else
                username="$2"
            fi
            ;;
    esac
    shift
done

# Create user.  If no user specified, use arcgis
# Set password to specified, otherwise "arcgis"
useradd -m -p "${password-arcgis}" "${username-arcgis}"

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

# Clear out old installation and content
rm -Rf /home/"$username"/arcgis
rm -Rf /data/arcgis
rm -f /data/*install.log
rm -Rf /home/*/.ESRI.properties*

# Remove and add entries to /etc/security/limits.conf
sed -i "/'$username'/d" /etc/security/limits.conf
echo -e "$username\t\t-\tnofile\t\t65535" >> /etc/security/limits.conf
echo -e "$username\t\t-\tnproc\t\t25059" >> /etc/security/limits.conf

# Delete previously set environmental variables from /etc/environment
sed -i '/ESRI_/d' /etc/environment
unset ESRI_SHARE
unset ESRI_VERSION
unset ESRI_USER

# Set environmental variables
echo "ESRI_SHARE=${share_path-/net/honeybadger/deploy}" >> /etc/environment
echo "ESRI_VERSION=${version}" >> /etc/environment
echo "ESRI_USER=${username-arcgis}" >> /etc/environment

exit 0