'''
"server" : {
    "hostname" : "machine.domain.com",
    "version" : "10.3",
    "username" : "arcgis",
    "password" : "arcgis",
    "install_dir" : "/data/arcgis",
    "config": {
        "content_dir" : "/data/arcgis/usr",
        "admin_user" : "siteadmin",
        "admin_pass" : "siteadmin",
        "auth_type" : "ldap",
        "auth_tier" : "web",
        "license" : "image",
        "webcontexturl" : "https://reverseproxy.domain.com/context",
        "webadaptorurl" : "https://webadaptor.domain.com/context",
        "site_machines" : [
            "server1.domain.com",
            "server2.domain.com"
        ],
        "geoevent" : true
    }
}

'''


class Server:
    def __init__(self, config):
        self.is_configured = False

        # Node info
        self.hostname = config["hostname"]
        self.version = config["version"]
        self.username = config["username"]
        self.password = config["password"]

        if config["config"]:
            self.config = config["config"]

    @abstractmethod
    def configure(self):
        pass

    @abstractmethod
    def restart(self):
        pass

    def add_machines(self):
        # TODO
        pass


class LinuxServer(Server):
    def __init__(self, config):
        super().__init__(config)
        # Create connection to linux node
        connection = LinuxConnection(self.hostname)

        try:
            # Check that install script exists on node
            path = "/root/.testbuilder/install_server.sh"
            if connection.validate_path(path) is None:
                if connection.copy_node_files() is None:
                    raise ValueError("Could not verify script files on node {} at {}".format(self.hostname, path))

            # Run install script on node
            log_path = "/root/.testbuilder/logs/install.log"
            cmd = "bash /root/.testbuilder/install_server.sh {} {} {}".format(config["install_dir"], self.version, self.username)
            if connection.submit(cmd) is None:
                raise ValueError("Could not install ArcGIS Server on {}. Check {} for errors".format(self.hostname, log_path))

            # Verify server manager is accessible
            url = "http://{}:6080/arcgis/manager".format(self.hostname)
            if util.validate_url(url) is None:
                raise ValueError("Could not access URL: {}".format(url))
            else:
                self.is_installed = True
        except Exception:
            raise

    def configure(self):
        # TODO
        pass

    def restart(self):
        # TODO
        pass


class WindowsServer(Server):
    def __init__(self, config):
        super().__init__(config)
        # Create connection to windows node
        connection = WindowsConnection(self.hostname, self.username, self.password)

        try:
            # Check that install script exists on node
            path = "%APPDATA%\.testbuilder\install_server.bat"
            if connection.validate_path(path) is None:
                if connection.copy_node_files() is None:
                    raise ValueError("Could not verify script files on node {} at {}".format(self.hostname, path))

            # Run install script on node
            log_path = r"%APPDATA%\testbuilder\logs\install.log"
            cmd = r"%APPDATA%\testbuilder\install_server.bat {} {}".format(config["install_dir"], self.version)
            if connection.submit(cmd) is None:
                raise ValueError("Could not install ArcGIS Server on {}. Check {} for errors".format(self.hostname, log_path))

            # Verify server manager is accessible
            url = "http://{}:6080/arcgis/manager".format(self.hostname)
            if util.validate_url(url) is None:
                raise ValueError("Could not access URL: {}".format(url))
            else:
                self.is_installed = True
        except Exception:
            raise

    def configure(self):
        # TODO
        pass

    def restart(self):
        # TODO
        pass


# Installs ArcGIS Server
# Requires: hostname, install_dir, version, username, password
def install_server(cfg):
    # Create connection to linux node
    if cfg["platform"] == "linux":
        connection = LinuxConnection(cfg["hostname"])
        script_path = "/root/.testbuilder/install_server.sh"
        log_path = "/root/.testbuilder/logs/install.log"
        cmd = "bash /root/.testbuilder/install_server.sh {} {} {}".format(cfg["install_dir"], cfg["version"], cfg["username"])

    # Create connection to windows node
    else:
        connection = WindowsConnection(cfg["hostname"], cfg["username"], cfg["password"])
        script_path = "%APPDATA%\.testbuilder\install_server.bat"
        log_path = r"%APPDATA%\testbuilder\logs\install.log"
        cmd = r"%APPDATA%\testbuilder\install_server.bat {} {}".format(config["install_dir"], cfg["version"])

        try:
            # Check that install script exists on node
            if connection.validate_path(script_path) is None:
                if connection.copy_node_files() is None:
                    raise ValueError("Could not verify script files on node {} at {}".format(cfg["hostname"], script_path))

            # Run install script on node
            if connection.submit(cmd) is None:
                raise ValueError("Could not install ArcGIS Server on {}. Check {} for errors".format(cfg["hostname"], log_path))

            # Verify server manager is accessible
            url = "http://{}:6080/arcgis/manager".format(cfg["hostname"])
            if util.validate_url(url) is None:
                raise ValueError("Could not access URL: {}".format(url))
        except Exception:
            raise