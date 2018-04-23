#!/bin/bash

if [ $# -ne 3 ]
then
    echo 'Usage: <script>.sh <version> <username> <installpath> <installershare>'
    exit 0
fi

version=$1
username=$2
install_path=$3
installer_share=$4
















# Update testbuilder_properties file
# TODO
prop_path = "home/${username}/.testbuilder_properties"
# "# $(date)" >> prop_path

# "datstore_install_dir=" >> prop_path
