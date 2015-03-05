from kippo.core.honeypot import HoneyPotCommand
from twisted.internet import reactor

commands = {}

class command_service(HoneyPotCommand):
    def start(self):
	if '--help' in self.args or '-h' in self.args or len(self.args) < 1:
            self.writeln('Usage: service < option > | --status-all | [ service_name [ command | --full-restart ] ]')
        elif '--status-all' in self.args:
            for l in (
                '[ + ]  acpid',
                '[ + ]  apache2',
                '[ - ]  apparmor',
                '[ ? ]  apport',
                '[ + ]  atd',
                '[ ? ]  console-setup',
                '[ + ]  cron',
                '[ - ]  dbus',
                '[ ? ]  dns-clean',
                '[ + ]  friendly-recovery',
                '[ - ]  grub-common',
                '[ ? ]  irqbalance',
                '[ ? ]  killprocs',
                '[ ? ]  kmod',
                '[ ? ]  networking',
                '[ ? ]  ondemand',
                '[ ? ]  pppd-dns',
                '[ - ]  procps',
                '[ ? ]  rc.digitalocean',
                '[ ? ]  rc.local',
                '[ + ]  resolvconf',
                '[ - ]  rsync',
                '[ + ]  rsyslog',
                '[ ? ]  screen-cleanup',
                '[ ? ]  sendsigs',
                '[ - ]  ssh',
                '[ - ]  sudo',
                '[ - ]  udev',
                '[ ? ]  umountfs',
                '[ ? ]  umountnfs.sh',
                '[ ? ]  umountroot',
                '[ - ]  unattended-upgrades',
                '[ - ]  urandom',):
                self.writeln(l)
        elif len(self.args) > 1:
            pass
        elif len(self.args) > 0:
            self.writeln('Usage: /etc/init.d/%s {start|stop|restart|force-reload|status}' % self.args[0])
        self.exit()
        return

commands['/usr/sbin/service'] = command_service
