import os
import imp
import time
import ftpassault
from ftpassault.config import Config

class Commands():
    def __init__(self):
        self.commands = {}
        self.get_commands()
        self.config = Config()

    def get_commands(self):
        # look in cmd directory for all commands
        path = '%s/cmd' % os.path.dirname(ftpassault.__file__)
        for module in os.listdir(path):
            if not module.startswith('__') and not module.endswith('.pyc'):
                # import found model and add to self.commands
                mod = imp.load_source('Cmd', os.path.join(path, module))
                # remove .py from module name and use that as key
                self.commands[module[:-3]] = mod.Cmd()

    def __call__(self, fs, ftp, cmd, args):
        # run given command
        try:self.commands[cmd](fs, ftp, args)
        except Exception as e:
            # if fail send 502 to client
            ftp.conn_send_and_log('502 not implemented.\r\n')
            print e
