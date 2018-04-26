import paramiko, wmi


class LinuxConnection:
    def __init__(self, hostname):
        self.hostname = hostname

        # paramiko connection
        self.connection = paramiko.SSHClient()

        # Determine correct root password for ECS instance
        try:
            ROOT_PASSWORDS = ["blue.jays", "red.sox", "lx.adm"] # set this globally, this is for testing
            for pw in ROOT_PASSWORDS:
                try:
                    self.connection.connect(self.hostname, 22, "root", pw)
                    self.password = pw
                except paramiko.AuthenticationException:
                    # if it's the last pw in the list, raise the exception
                    if ROOT_PASSWORDS[-1] == pw:
                        raise
                    else:
                        continue
        except Exception:
            raise

        self.connection.close()

    def submit(self, cmd):
        try:
            self.connection.connect(self.hostname,22,"root", self.password)
            response = self.connection.exec_command(cmd)
            self.connection.close()
            # get result from response
            # TODO
            result = response # TODO

            return result
        except Exception:
            raise


class WindowsConnection:
    def __init__(self, hostname, platform, username, password):
        self.hostname = hostname
        self.platform = platform
        self.username = username
        self.password = password

    def submit(self, cmd):
        try:
            self.connection.connect( # TODO
            response = self.connection.exec_command(cmd)
            self.connection.close() # TODO Needed?
            # get result from response
            # TODO
            result = response # TODO

            return result
        except Exception:
            raise




'''import paramiko

root_passwords = ["blue.jays", "red.sox", "lx.adm"]

class Connection:
    def __init__(self, hostname, os_type, username=None, password=None):
        self.os_type = os_type
        self.hostname = hostname

        # Create a connection to a Linux machine
        if self.os_type == "linux":
            self.__client = paramiko.SSHClient()
            self.__client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Create a connection to a Windows machine
        else:
            self.__username = username
            self.__password = password

            # TODO use wmi or winrm module to create a connection
            pass


    def connect(self):
        if self.os_type == "linux":
            for pw in root_passwords:
                try:
                    self.__client.connect(self.hostname,22,"root",pw)
                    break

                except paramiko.AuthenticationException:
                    continue

                except Exception:
                    raise

            return True

        else:
            # TODO connect to windows machine
            pass


    def disconnect(self):
        if self.os_type == "linux":
            try:
                self.__client.close()
                return True

            except Exception:
                raise

        else:
            # TODO close windows connection
            pass


    def submit(self, commands):
        if self.os_type == "linux":
            try:
                results = []
                for cmd in commands:
                    results.append(self.__client.exec_command(cmd))

                return results

            except Exception:
                raise

        else:
            # TODO submit commands to windows machine
            pass