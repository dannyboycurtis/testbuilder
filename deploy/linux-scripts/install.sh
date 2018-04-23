#!/bin/bash

if [ $# -lt 4 ]
then
    echo 'Usage: install.sh <product> <version> <install_dir> <username>'
    exit 0
fi

case "$2" in
    "10.3"|"10.3.1"|"10.4"|"10.4.1"|"10.5"|"10.5.1"|"10.6")
        version = $2
        break
        ;;
    *)
        echo "Supported versions: 10.3 - 10.6"
        exit 0

if ! [ "$3" =~ ^(/[^/ ]*)+/?$ ]
then
    echo "${3} is not a valid Linux path"
    exit 0
else
    install_dir = $3
fi

username = $4

installer_path = $( cat /root/.testbuilder/settings|grep installer_path|cut -d '=' -f 2)
if ! [ -e ${installer_path} ]
then
    echo "Unable to access installers at ${installer_path}"
    exit 0
fi

case "$1" in
    server)
        install_server
        ;;
    portal)
        install_portal
        ;;
    datastore)
        install_datastore
        ;;
    webadaptor)
        install_webadaptor
        ;;
    tomcat)
        install_tomcat
        ;;
    httpd)
        install_httpd
        ;;
    *)
    echo "Available products: server | portal | datastore | webadaptor | tomcat | httpd"
    exit 0

function create_path {
    rm -Rf "$install_dir"
    mkdir -p "$installdir"
    if [ -d "$install_dir" ]
    then
        return 1
    else
        echo "Unable to create installation directory"
        return 0
    fi
}

function install_server {
    if [ create_path != 1 ]
    then
        echo "Server installation failed!"
        exit 0
    else
        sudo -c ${username} sh ${installer_path}/install/${version}/server/Setup.sh -m silent -l yes -d ${install_dir}
        result = $(wget -S "http://localhost:6080/arcgis/manager" 2>&1 | grep "HTTP/" | awk '{print $2}')
        if [ "$result" != 200 ]
        then
            echo "Server Manager page inaccessible: http://localhost:6080/arcgis/manager"
            echo "Server installation failed!"
            exit 0

        exit 1
}

function install_portal {
    if [ create_path != 1 ]
    then
        echo "Portal installation failed!"
        exit 0
    else
        sudo -c ${username} sh ${installer_path}/install/${version}/portal/Setup.sh -m silent -l yes -d ${install_dir}
        sleep 60  # TODO fine tune this sleep time
        result = $(wget -S "https://localhost:7443/arcgis/home" 2>&1 | grep "HTTP/" | awk '{print $2}')
        if [ "$result" != 200 ]
        then
            echo "Portal Home page inaccessible: https://localhost:7443/arcgis/home"
            echo "Portal installation failed!"
            exit 0

        exit 1

}

function install_datastore {
    if [ create_path != 1 ]
    then
        echo "Datastore installation failed!"
        exit 0
    else
        sudo -c ${username} sh ${installer_path}/install/${version}/datastore/Setup.sh -m silent -l yes -d ${install_dir}
        result = $(wget -S "https://localhost:2443/arcgis/datastore" 2>&1 | grep "HTTP/" | awk '{print $2}')
        if [ "$result" != 200 ]
        then
            echo "Datastore Configuration page inaccessible: http://localhost:6080/arcgis/manager"
            echo "Datastore installation failed!"
            exit 0
        fi
    fi
    exit 1

}

function install_webadaptor {
    if [ create_path != 1 ]
    then
        echo "Webadaptor installation failed!"
        exit 0
    else
        sudo -c ${username} sh ${installer_path}/install/${version}/webadaptor/java/Setup.sh -m silent -l yes -d ${install_dir}
    fi
    exit 1
}

function install_tomcat {


}

function install_httpd {


}