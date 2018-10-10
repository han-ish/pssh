import pexpect
import uuid
import logging
import os


FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
path = os.path.dirname(os.path.abspath(__file__))
file_ = os.path.join(path, os.path.basename(__file__))
filename = "{}.log".format(os.path.splitext(file_)[0])
logging.basicConfig(filename=filename, mode='w', format=FORMAT)
logger = logging.getLogger(__name__)


class Session(object):
    """
    A highlevel wrapper for session with an SSH server using pexpect

    client = Session("foo", "s3cr3t", "172.16.8.38")
    stdout = client.exec_command("ls")
    """
    def __init__(self, username, password, hostname):
        """
        Create a new SSH client session

        :param str username: username for logging into the server
        :param str password: password for logging into the server
        :param str hostname: hostname of the server
        """
        self.username = username
        self.password = password
        self.hostname = hostname
        self.login()

    def login(self):
        self.expected_at_login = ['Are you sure you want to continue connecting', '.*assword:', pexpect.EOF]
        self.session = pexpect.spawn("ssh {}@{}".format(self.username, self.hostname))

        index = self.session.expect(self.expected_at_login)
        # accept the remote key
        if index == 0:
            self.session.sendline("yes")
            index = self.session.expect(self.expected_at_login)
        if index == 1:
            self.session.sendline(self.password)
        if index == 2:
            raise ValueError("Failed to login")

        # for logging in and reading the buffer
        self.session.expect([r'.*\$ ', r'.*\# ', pexpect.TIMEOUT, pexpect.EOF], timeout=2)
        logger.debug(self.session.before)

        # setting new prompt and initializing a new bash session
        # without any colors or styles
        self.prompt = str(uuid.uuid4())
        self.session.sendline('PS1="{}" bash -norc'.format(self.prompt))

        # expecting prompt twice because the buffer may have
        # the PS1 while setting and when getting the prompt
        self.session.expect_exact(self.prompt)
        self.session.expect_exact(self.prompt)
        self.session.sendline('alias ls="ls -1"'.format(self.prompt))
        self.session.expect_exact(self.prompt)

    def exec_command(self, command, expected=None, timeout=2):
        """
        Execute command on the SSH server.

        :param str command: a shell command to execute.
        :param str command:
            expected string for the command.
            Eg:- for command `tail -f ` with `grep` or similar
        :param int timeout:
            set the timeout for the executed command

        :return:
            stdout of the executed command as list of lines
        :raises:
            No exception for now
        """
        command = r'{}'.format(command)
        self.session.sendline(command)
        if expected:
            self.session.expect(expected)
            #self.session.expect_exact(self.prompt)
            #else:
        self.session.expect_exact(self.prompt)
        stdout = self.session.before.strip().split('\r\n')

        # the first line will be the command itself
        return stdout[1:]

    def close(self):
        """
        Close the session
        """
        self.session.sendline("exit")

