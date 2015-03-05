from kippo.core.honeypot import HoneyPotCommand
from kippo.core.fs import HoneyPotFilesystem
from twisted.internet import reactor

commands = {}

class command_which(HoneyPotCommand):
    def start(self):
        paths = ['', '/bin/', '/usr/bin/', '/sbin/', '/usr/sbin/']
        for arg in self.args:
            for path in paths:
                if self.fs.exists(path + arg):
                    self.writeln(path+arg)
        self.exit()
        return

commands['/usr/bin/which'] = command_which
