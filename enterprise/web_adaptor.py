'''
"webadaptor" : {
    "hostname" : "machine.domain.com",
    "platform" : "linux"
    "version" : "10.3",
    "username" : "arcgis",
    "password" : "arcgis",
    "install_dir": "/data/arcgis",
    "type": "java",
    "context": "arcgis",
    "mode": "server",
    "admin_access": true,
    "gis_host": "hostname.domain.com",
    "sso": false,
    "http_port": "80",
    "https_port": "443"
}

'''


def install_webadaptor(cfg):
    if cfg["platform"] == "linux":
        # Create connection to linux node
        connection = LinuxConnection(cfg["hostname"])
        script_path = "/root/.testbuilder/install_webadaptor.sh"
        log_path = "/root/.testbuilder/logs/install.log"
        cmd = "bash /root/.testbuilder/install_webadaptor.sh {} {} {}".format(cfg["install_dir"], cfg["version"], cfg["username"])
    else:
        # Create connection to windows node
        connection = WindowsConnection(cfg["hostname"], cfg["username"], cfg["password"])
        script_path = "%APPDATA%\.testbuilder\install_webadaptor.bat"
        log_path = r"%APPDATA%\testbuilder\logs\install.log"
        cmd = r"%APPDATA%\testbuilder\install_webadaptor.bat {} {}".format(cfg["install_dir"], cfg["version"])

    try:
        # Check that install script exists on node
        if connection.validate_path(script_path) is None:
            if connection.copy_node_files() is None:
                raise ValueError("Could not verify script files on node {} at {}".format(cfg["hostname"], script_path))

        # Run install script on node
        if connection.submit(cmd) is None:
            raise ValueError(
                "Could not install web adaptor on {}. Check {} for errors".format(cfg["hostname"], log_path))

        # Verify webadaptor config page is accessible
        if util.validate_url(url) is None:
            raise ValueError("Could not access URL: {}".format(url))
        else:
            self.is_installed = True
    except Exception:
        raise
