#!/bin/bash

if [ $# -lt 1 ] || [ $# -gt 2 ]; then
    echo "Usage: tomcat.sh -v 7.0.62 -http 80 -https 443"
    exit 0
fi

# Check for options
while [ $# -gt 0 ]
do
    case $1 in
        -v)
            # Check for valid version and set version to it
            if [ "${2:0:3}" != "7.0" ] || [ "${2:0:2}" != "8." ]; then
                echo "Valid version: 7.0.x | 8.x.x"
                exit 0
            else
                version=$2
            fi
            ;;
        -http)
            # Set http_port
            http_port=$2
            ;;
        -https)
            # Set https_port
            https_port=$2
            ;;
    esac
    shift
done

# Set highest supported version for ESRI_VERSION if version not set
case $ESRI_VERSION in
    "10.3"|"10.3.1")
        version=${version-7.0.22}
        ;;
    "10.4"|"10.4.1")
        version=${version-7.0.65}
        ;;
    "10.5"|"10.5.1")
        version=${version-7.0.72}
        ;;
    "10.6"|"10.6.1")
        version=${version-7.0.82}
        ;;
    *)
        version=7.0.82
esac

# Install Java 8 from share
echo "Installing Java 8 to /data/java"
tar -xvf $ESRI_SHARE/install/java/jre-8u171-linux-x64.tar.gz -C /data/java/
ESRI_JAVA=/data/java/bin
export $ESRI_JAVA
./data/java/bin/java -version
if [ $? != 0 ]; then
    echo "Java installation failed"

# Set http/https ports if not specified
echo "$(date) : Installing Tomcat $version to /data/tomcat"
echo "$(date) : Tomcat ports set to $http_port/$https_port"
http_port=${http_port-80}
https_port=${https_port-443}

# Check if tomcat version exists in file share, otherwise download it to the file share
if [ -e "$ESRI_SHARE/install/tomcat/apache-tomcat-$version.tar.gz" ]; then
    echo "Using Tomcat $version from $ESRI_SHARE"
    cp -R "$ESRI_SHARE/install/tomcat/apache-tomcat-$version.tar.gz" /data/
else
    echo "Downloading Tomcat $version from archive.apache.org"
    url="http://archive.apache.org/dist/tomcat/tomcat-${version:0:1}/v$version/bin/apache-tomcat-$version.tar.gz"

    result=$(wget -q --spider "$url")
    if [ $? == 0 ]; then
        echo "Tomcat $version download unavailable: $url"
        exit 1
    else
        # Download version and copy to ESRI_SHARE for future use
        wget -q "$url" -O "/data/apache-tomcat-$version.tar.gz"
        cp /data/apache-tomcat-$version.tar.gz "$ESRI_SHARE/install/tomcat/"
    fi
fi

# Untar Tomcat
rm -Rf /data/tomcat
mkdir /data/tomcat
tar -xvf /data/apache-tomcat-$version.tar.gz -C /data/
CATALINA_HOME="/data/apache-tomcat-$version/bin"
export CATALINA_HOME
echo "Setting CATALINA_HOME to /data/apache-tomcat-$version/bin"

# Copy keystore with wildcard cert to machine
cp "$ESRI_SHARE/config/ssl/keystore" "/root/keystore"

# Copy server.xml from ESRI_SHARE to Tomcat installation
mv /data/tomcat/conf/server.xml /data/tomcat/conf/server.xml.backup
case $version in
    7*)
        cp "$ESRI_SHARE/config/tomcat/server7.xml" /data/tomcat/conf/server.xml
        ;;
    8.0*)
        cp "$ESRI_SHARE/config/tomcat/server8.xml" /data/tomcat/conf/server.xml
        ;;
    8.5*)
        cp "$ESRI_SHARE/config/tomcat/server85.xml" /data/tomcat/conf/server.xml
        ;;
esac

# Update server.xml with http_port and https_port
sed -i "s/8080/$http_port/" /data/tomcat/conf/server.xml
sed -i "s/8443/$https_port/" /data/tomcat/conf/server.xml

# Move arcgistomcat.service file to /etc/systemd/system and configure service
cp "$ESRI_SHARE/config/tomcat/arcgistomcat.service" /etc/systemd/system/arcgistomcat.service
systemctl enable arcgistomcat.service
systemctl start arcgistomcat.service
echo $(systemctl status arcgistomcat.service)

# Confirm the tomcat splash page is accessible at the http port
wget --spider -q "http://localhost:$http_port"
if [ $? != 0 ]; then
    echo "Failed to access http://localhost:$http_port"
else
    echo "http://localhost:$http_port is accessible"
fi

# Confirm the tomcat splash page is accessible at the https port
wget --spider -q --no-check-certificate "https://localhost:$https_port"
if [ $? != 0 ]; then
    echo "Failed to access https://localhost:$https_port"
else
    echo "https://localhost:$https_port is accessible"
fi

exit 0