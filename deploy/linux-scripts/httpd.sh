#!/bin/bash

# Required input arguments for script
if [[ $# -eq 0 ]] ; then
    echo 'Usage: <script>.sh <> <password>'
    exit 0
fi

# Check OS
case $(lsb_release -s -i| tr "[A-Z]" "[a-z]") in
    "centos"|"oracleserver"|"redhatenterpriseserver"|"scientific")
        yum --y install httpd openssl
        configure_httpd()
        ;;
    "ubuntu")
        apt-get -y install apache2 openssl
        configure_apache2()
        ;;
    "suse linux")
        # TODO Need to test this
        zypper -n install httpd openssl
        configure_httpd()
        ;;
    *)
        exit
        ;;
esac


function configure_httpd {
    # TODO Configure SSL on httpd and set up wildcard certificate

    systemctl enable httpd.service
    systemctl restart httpd.service
}

function configure_apache2 {
    # TODO Configure SSL on apache2 and set up wildcard certificate

    systemctl enable apache2.service
    systemctl restart apache2.service
}
