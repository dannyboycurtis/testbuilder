# config = {
#   "platform": "linux" | "windows',
#   "hostname": "fsmachine.domain.com",
#   "roles": [ "portal" &| "server" &| "data" ]
# }


def create_fileshare(connection, roles):
    # Check if fileshare.sh is present on machine, copy over if not
    try:
        path = "/home/{}/.testbuilder/fileshare.sh".format(connection.hostname)
        result = connection.validate_path(path)
    except Exception:
        raise

    if result is None:


    # If result is 0, copy fileshare.sh over to machine
    # TODO read in stdout from result and check for 1 or 0
    if result is None:
        cmd = ""



