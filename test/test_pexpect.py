from typing import TextIO

import pexpect, tempfile

def ssh(host, cmd, user, password, timeout=30, bg_run=False):
    """SSH'es to a host using the supplied credentials and executes a command.
    Throws an exception if the command doesn't return 0.
    bgrun: run command in the background"""

    fname = tempfile.mktemp()
    fout = open(fname, 'wb')

    options = '-q -oStrictHostKeyChecking=no -oUserKnownHostsFile=/dev/null -oPubkeyAuthentication=no'
    if bg_run:
        options += ' -f'
    options = ""
    ssh_cmd = 'ssh {}@{} {} {}'.format(user, host, options, cmd)
    child = pexpect.spawn(ssh_cmd, timeout=60)
    child.expect(['password: '])
    child.sendline(password)
    child.logfile = fout
    child.expect(pexpect.EOF)
    child.close()
    fout.close()

    fin = open(fname, 'r')  # type: TextIO
    stdout = fin.read()
    fin.close()

    if 0 != child.exitstatus:
        raise Exception(stdout)

    return stdout



result = ssh("localhost", "pwd;pwd", "arcgis", "mushroom")

print("result:\n" + result.strip('\n'))