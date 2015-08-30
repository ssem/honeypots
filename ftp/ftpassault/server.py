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
            os.setuid(running_uid)
            os.setgid(running_gid)
            old_umask = os.umask(077)

    def serve(self, port, welcome):
        try:
            self.socket.bind(('', int(port)))
            self.socket.listen(0)
            print "Listening on: %s" % port
        except socket.error as e:
            if e.errno == 13:
                exit("Ports below 1024 must run as root")
            raise e
        self.drop_privs()
        while True:
            try:
                # check if any cmds want us to disconnect
                if self.session.disconnect:
                    raise Exception("disconnect")
                # check if we have a connection, if not wait for one
                if self.session.conn is None:
                    self.session.conn, addr = self.socket.accept()
                    # open log file for new connection
                    self.session.open_log_file(addr)
                    self.session.conn_send_and_log(welcome+'\r\n')
                recv = self.session.conn_recv_and_log(256)
                if recv == '':
                    raise Exception("no command")
                # parse client command
                cmd = recv[:4].strip().upper()
                # parse client args
                args = recv[4:].lstrip(' ').rstrip('\r\n')
                print "[+] CMD", cmd, args
                # if client is attempting to log in or is authenticated run command
                if cmd == 'AUTH' or cmd == 'USER' or cmd == 'PASS' or self.session.authenticated:
                    self.commands(self.fs, self.session, cmd, args)
            except KeyboardInterrupt:
                exit("Bye")
            except Exception as e:
                print "[-] SERVER", str(e)
                if str(e) != "no command" and str(e) != "disconnect":
                    error_log = open(os.path.join(self.conf.log_path, "server_error"), "w+")
                    error_log.write(str(e))
                    error_log.close()
                # if exception close everything and restart
                try:self.session.data.close()
                except:pass
                try:self.session.conn.close()
                except:pass
                try:self.session._log_file.close()
                except:pass
                try:self.session = Session()
                except:pass

    def __del__(self):
        # on exit attempt to save the filesystem and close sockets
        try:self.fs.save()
        except:pass
        try:self.session._log_file.close()
        except:pass
        try:self.session.conn.close()
        except:pass
        try:self.socket.close()
        except:pass

