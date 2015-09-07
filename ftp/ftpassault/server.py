import os
import pwd
import grp
import socket
from ftpassault.config import Config
from ftpassault.session import Session
from ftpassault.commands import Commands
from ftpassault.file_system import File_System


class Ftp():
    def __init__(self, fs_path):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conf = Config()
        self.commands = Commands()
        self.fs = File_System(fs_path)
        self.session = Session()

    def drop_privs(self):
        if os.getuid() == 0:
            try:
                running_uid = pwd.getpwnam(self.conf.privs).pw_uid
                running_gid = grp.getgrnam(self.conf.privs).gr_gid
            except Exception as e:
                exit("Can not drop privileges user does not exist: %s" % self.conf.privs)
            os.setgroups([])
            os.setgid(running_gid)
            os.setuid(running_uid)
            old_umask = os.umask(077)

    def serve(self, port, welcome):
        self.session.bind(("", int(port)))
        self.session.listen(0)
        print "Listening on: %s" % port
        self.drop_privs()
        while True:
            try:
                if self.session.conn is None:
                    self.session.accept()
                    self.session.send(welcome+'\r\n')
                message = self.session.recv(256)
                try:cmd = message[:4].strip().upper()
                except:cmd = ''
                try:args = message[4:].lstrip(' ').rstrip('\r\n')
                except:args = ''
                print "[+] CMD", cmd, args
                if cmd == 'AUTH' or cmd == 'USER' or cmd == 'PASS' or self.session.authenticated:
                    self.commands(self.fs, self.session, cmd, args)
                else:
                    self.session.close()
            except KeyboardInterrupt:
                exit("Bye")
            except Exception as e:
                print "[-] SERVER", str(e)
                error_log = open(os.path.join(self.conf.log_path, "server_error"), "w+")
                error_log.write(str(e))
                error_log.close()
                self.session.close()

    def __del__(self):
        self.fs.save()
        #except:print "[-] Error saving file system"
        self.session.close()

