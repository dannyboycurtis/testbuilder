'''"
"portal": {
    "hostname" : "machine.domain.com",
    "version" : "10.3",
    "username" : "arcgis",
    "password" : "arcgis",
    "install_dir": "/data/arcgis",
    "config": {
        "content_dir": "/net/hostname/share/content",
        "admin_username": "portaladmin",
        "admin_password": "portaladmin1",
        "security_question": "Your favorite ice cream flavor?",
        "security_answer": "vanilla",
        "auth_type": "ldap",
        "auth_tier": "web",
        "auto_account_creation": true,
        "webcontext_url": "https://reverseproxy.domain.com/context",
        "webadaptor_url": "https://webadaptor.domain.com/context",
        "federation": [
            {
              "type": "imageHosting",
              "is_hosting": false,
              "gis_host": "arcgisserver.domain.com",
              "psa_username": "siteadmin",
              "psa_password": "siteadmin"
            },
            {
              "type": null,
              "is_hosting": true,
              "gis_host": "arcgisserver.domain.com",
              "psa_username": "siteadmin",
              "psa_password": "siteadmin"
            }
        ],
        "portal_ha": {
            "rank": "primary",
            "portal_host": "portal2.domain.com",
            "private_portal_url": "https://internalLB.domain.com:7443"
        }
    }
}
'''


class Portal:
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

    def configure_ha(self):
        # TODO
        pass

    def federate(self):
        # TODO
        pass


class LinuxPortal(Portal):
    def __init__(self, config):
        super().__init__(config)
        # Create connection to linux node
        connection = LinuxConnection(self.hostname)

        try:
            # Check that install script exists on node
            path = "/root/.testbuilder/install_portal.sh"
            if connection.validate_path(path) is None:
                if connection.copy_node_files() is None:
                    raise ValueError("Could not verify script files on node {} at {}".format(self.hostname, path))

            # Run install script on node
            log_path = "/root/.testbuilder/logs/install.log"
            cmd = "bash /root/.testbuilder/install_portal.sh {} {} {}".format(config["install_dir"], self.version,
                                                                              self.username)
            if connection.submit(cmd) is None:
                raise ValueError(
                    "Could not install Portal for ArcGIS on {}. Check {} for errors".format(self.hostname, log_path))

            # Verify portal home is accessible
            url = "https://{}:7443/arcgis/home".format(self.hostname)
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


class WindowsPortal(Portal):
    def __init__(self, config):
        super().__init__(config)
        # Create connection to windows node
        connection = WindowsConnection(self.hostname, self.username, self.password)

        try:
            # Check that install script exists on node
            path = "%APPDATA%\.testbuilder\install_portal.bat"
            if connection.validate_path(path) is None:
                if connection.copy_node_files() is None:
                    raise ValueError("Could not verify script files on node {} at {}".format(self.hostname, path))

            # Run install script on node
            log_path = r"%APPDATA%\testbuilder\logs\install.log"
            cmd = r"%APPDATA%\testbuilder\install_portal.bat {} {}".format(config["install_dir"], self.version)
            if connection.submit(cmd) is None:
                raise ValueError(
                    "Could not install Portal for ArcGIS on {}. Check {} for errors".format(self.hostname, log_path))

            # Verify portal home is accessible
            url = "https://{}:7443/arcgis/home".format(self.hostname)
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
