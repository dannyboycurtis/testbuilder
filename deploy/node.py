from utilities import connection



class Node:
    def __init__(self, config):
        self.is_configured = False

        # Read in configuration values
        self.hostname = config["hostname"]
        self.username = config["username"]
        self.password = config["password"]
        self.platform = config["platform"]
        self.version = config["version"]

        if self.platform is "linux":
            self.node_path = r"/root/.testbuilder/"
        else:
            self.node_path = r"%APPDATA%\.testbuilder\"

        self.install_log = "{}install.log".format(self.node_path)
        self.config_log = "{}config.log".format(self.node_path)

        self.components = config["enterprise"]


        # Copy scripts and blank property file to node


        # Run node script to prepare machine
        # Create connection to node based on platform and set platform-specific strings
        if self.platform == "linux":
            connection = LinuxConnection(self.hostname)
            cmd = "bash {}prepare_node.sh {} {}".format(script_path,self.username, self.password)
        else:
            connection = WindowsConnection(self.hostname, self.username, self.password)
            cmd = "{}prepare_node.bat {} {}".format(script_path, self.username, self.password)

        try:
            # Copy configuration directory onto node
            if self.copy_node_files() is None:
                raise ValueError("Could not copy script files on node {} at {}".format(self.hostname, script_path))

            # Run install script on node
            if connection.submit(cmd) is None:
                raise ValueError("Could not prepare node. Check {} on machine".format(self.install_log))
        except Exception:
            raise

        # Determine components


        # Install components
        if self.platform == "linux":
            # install components using multi-threading

        else:
            # install components one at a time

        # Configure components using multi-threading


        # Verify node completion


    def install_server(self, install_dir):
        # Create connection to node based on platform and set platform-specific strings
        if self.platform == "linux":
            connection = LinuxConnection(self.hostname)
            cmd = "bash {}install_server.sh {} {} {}".format(self.node_path, install_dir, self.version, self.username)
        else:
            connection = WindowsConnection(self.hostname, self.username, self.password)
            cmd = "{}install_server.bat {} {} {}".format(self.node_path, install_dir, self.version, self.username)

        try:
            # Run install script on node
            if connection.submit(cmd) is None:
                raise ValueError("Could not install ArcGIS Server on {}. Check {} for errors".format(self.hostname, self.install_log))

            # Verify server manager is accessible
            url = "http://{}:6080/arcgis/manager".format(self.hostname)
            if util.validate_url(url) is None:
                raise ValueError("ArcGIS Server installation incomplete. Check {} for errors".format(url, self.install_log))
        except Exception:
            raise

    def install_portal(self, install_dir):
        # Create connection to node based on platform and set platform-specific strings
        if self.platform == "linux":
            connection = LinuxConnection(self.hostname)
            cmd = "bash {}install_portal.sh {} {} {}".format(self.node_path, install_dir, self.version, self.username)
        else:
            connection = WindowsConnection(self.hostname, self.username, self.password)
            cmd = "{}install_portal.bat {} {} {}".format(self.node_path, install_dir, self.version, self.username)

        try:
            # Run install script on node
            if connection.submit(cmd) is None:
                raise ValueError("Could not install Portal for ArcGIS on {}. Check {} for errors".format(self.hostname, self.install_log))

            # Verify portal home is accessible
            url = "https://{}:7443/arcgis/home".format(self.hostname)
            if util.validate_url(url) is None:
                raise ValueError("Portal for ArcGIS installation incomplete. Check {} for errors".format(url, self.install_log))
        except Exception:
            raise

    def install_datastore(self, install_dir):
        # Create connection to node based on platform and set platform-specific strings
        if self.platform == "linux":
            connection = LinuxConnection(self.hostname)
            cmd = "bash {}install_datastore.sh {} {} {}".format(self.node_path, install_dir, self.version, self.username)
        else:
            connection = WindowsConnection(self.hostname, self.username, self.password)
            cmd = "{}install_datastore.bat {} {} {}".format(self.node_path, install_dir, self.version, self.username)

        try:
            # Run install script on node
            if connection.submit(cmd) is None:
                raise ValueError("Could not install ArcGIS Datastore on {}. Check {} for errors".format(self.hostname, self.install_log))

            # Verify portal home is accessible
            url = "https://{}:2443/arcgis/datastore".format(self.hostname)
            if util.validate_url(url) is None:
                raise ValueError("ArcGIS Datastore installation incomplete. Check {} for errors".format(url, self.install_log))
        except Exception:
            raise

    def install_webadaptor(self, webadaptor):
        # Create connection to node based on platform and set platform-specific strings
        if self.platform == "linux":
            connection = LinuxConnection(self.hostname)
            cmd = "bash {}install_webadaptor.sh {} {} {}".format(self.node_path, webadaptor["install_dir"], self.version, self.username)
        else:
            connection = WindowsConnection(self.hostname, self.username, self.password)
            cmd = "{}install_webadaptor.bat {} {} {}".format(self.node_path, webadaptor["install_dir"], self.version, self.username)

        try:
            # Run install script on node
            if connection.submit(cmd) is None:
                raise ValueError("Could not install web adaptor on {}. Check {} for errors".format(self.hostname, self.install_log))

            # Verify portal home is accessible
            url = "https://{}:{}/{}/webadaptor".format(self.hostname, webadaptor["https_port"], webadaptor["context"])
            if util.validate_url(url) is None:
                raise ValueError("Web adaptor installation incomplete. Check {} for errors".format(url, self.install_log))
        except Exception:
            raise

    def configure_server(self):
        if int(self.version[:4]) >= 10.6:
            # Connect to machine and configure using command line
        else:
            # Use POST requests to configure Server
        pass

    def configure_portal(self):
        if int(self.version[:4]) >= 10.6:
            # Connect to machine and configure using command line
        else:
            # Use POST requests to configure Portal
        pass

    def configure_datastore(self):
        # Connect to machine and configure using command line
        pass

    def configure_webadaptor(self):
        # Connect to machine and configure using command line
        pass

    def configure_webserver(self):
        pass

    def create_fileshare(self):
        pass

    def validate_path(self, path):
        if self.platform == "linux":
            connection = LinuxConnection(self.hostname)
            cmd = "if [ -d {} ]; then echo 'true'; fi".format(path),

        else:
            connection = WindowsConnection(self.hostname, self.username, self.password)
            cmd = "IF EXIST {} ECHO true".format(path)

        try:
            return connection.submit(cmd)
        except Exception:
            raise

    def copy_node_files(self):
        pass