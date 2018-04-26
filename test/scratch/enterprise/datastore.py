'''
"datastore": {
    "hostname" : "machine.domain.com",
    "version" : "10.3",
    "username" : "arcgis",
    "password" : "arcgis",
    "install_dir" : "/data/arcgis",
    "config" : {
        "content_dir": "/data/arcgis/datastore/usr/datastore",
        "types": [
            "relational",
            "tilecache",
            "spatiotemporal"
        ],
        "gis_host": "arcgisserver.domain.com",
        "rank": "primary"
    }
}
'''

class Datastore:
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


class LinuxDatastore(Datastore):
    def __init__(self, config):
        super().__init__(config)
        # Create connection to linux node
        connection = LinuxConnection(self.hostname)

        try:
            # Check that install script exists on node
            path = "/root/.testbuilder/install_datastore.sh"
            if connection.validate_path(path) is None:
                if connection.copy_node_files() is None:
                    raise ValueError("Could not verify script files on node {} at {}".format(self.hostname, path))

            # Run install script on node
            log_path = "/root/.testbuilder/logs/install.log"
            cmd = "bash /root/.testbuilder/install_datastore.sh {} {} {}".format(config["install_dir"], self.version, self.username)
            if connection.submit(cmd) is None:
                raise ValueError(
                    "Could not install ArcGIS Datastore on {}. Check {} for errors".format(self.hostname, log_path))

            # Verify datastore config page is accessible
            url = "https://{}:2443/arcgis/datastore".format(self.hostname)
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


class WindowsDatastore(Datastore):
    def __init__(self, config):
        super().__init__(config)
        # Create connection to windows node
        connection = WindowsConnection(self.hostname, self.username, self.password)

        try:
            # Check that install script exists on node
            path = "%APPDATA%\.testbuilder\install_datastore.bat"
            if connection.validate_path(path) is None:
                if connection.copy_node_files() is None:
                    raise ValueError("Could not verify script files on node {} at {}".format(self.hostname, path))

            # Run install script on node
            log_path = r"%APPDATA%\testbuilder\logs\install.log"
            cmd = r"%APPDATA%\testbuilder\install_datastore.bat {} {}".format(config["install_dir"], self.version)
            if connection.submit(cmd) is None:
                raise ValueError(
                    "Could not install ArcGIS Datastore on {}. Check {} for errors".format(self.hostname, log_path))

            # Verify datastore config page is accessible
            url = "https://{}:2443/arcgis/datastore".format(self.hostname)
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
