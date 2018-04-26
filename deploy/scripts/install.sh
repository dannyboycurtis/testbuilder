#!/bin/bash

if [ $# -lt 1 ] || [ $# -gt 3 ]; then
    echo "Usage: install.sh <product> -v 10.x.x"
    exit 1
fi

if [ $1 != "server" ] && [ $1 != "portal" ] && [ $1 != "datastore" ] && [ $1 != "webadaptor" ]; then
    echo "Valid products: server | portal | datastore | webadaptor"
    exit 1
fi

product=$1

# Check for valid version
if [ $2 == "-v" ]; then
    if [ $(echo "$3"|cut -d '.' -f 1) -ne "10" ] || [ $(echo "$3"|cut -d '.' -f 2) -lt 3 ]; then
        if ! [ -v $ESRI_VERSION ]; then
            echo "Cannot determine version.  Use '-s 10.x.x'"
            exit 1
        fi
        version="$ESRI_VERSION"
    fi
    version="$3"
fi

user=${ESRI_USER-arcgis}
# If user does not exist, create arcgis
id -u "$user"
if [ $? != "0" ]; then
    useradd -m -p "arcgis" arcgis
    ESRI_USER="$user"
    export ESRI_USER
fi

share=${ESRI_SHARE-/net/honeybadger/deploy}

# Run installer
sh -c "$user" "$share/install/arcgis/$version/$product/Setup.sh" -m silent -l yes -d /data/arcgis -v >> "/data/$product_install.log"

# Move arcgis* service file to /etc/systemd/system and configure service
if [ $1 != "webadaptor" ]; then
    cp "$ESRI_SHARE/config/arcgis/arcgis$product.service" "/etc/systemd/system/arcgis$product.service"
    systemctl enable "arcgis$product.service"
    systemctl start "arcgis$product.service"
    echo $(systemctl status "arcgis$product.service")
fi

exit 0
