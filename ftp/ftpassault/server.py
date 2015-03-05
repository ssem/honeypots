import socket
from ftpassault.session import Session
from ftpassault.commands import Commands
from ftpassault.file_system import File_System


class Ftp():
    def __init__(self, fs_path):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.commands = Commands()
        self.fs = File_System(fs_path)
        self.session = Session()

    def serve(self, port, welcome):
        self.socket.bind(('', int(port)))
        self.socket.listen(0)
        while True:
            try:
                # check if any cmds want us to disconnect
                if self.session.disconnect:
                    raise Exception
                # check if we have a connection if not wait for one
                if self.session.conn is None:
                    self.session.conn, addr = self.socket.accept()
                    # open log file for new connection
                    self.session.open_log_file(addr)
                    self.session.conn_send_and_log(welcome+'\r\n')
                recv = self.session.conn_recv_and_log(256)
                if recv == '':
                    raise Exception
                # parse client command
                cmd = recv[:4].strip().upper()
                # parse client args
                args = recv[4:].lstrip(' ').rstrip('\r\n')
                # if client is attempting to log in or is authenticated run command
                if cmd == 'USER' or cmd == 'PASS' or self.session.authenticated:
                    self.commands(self.fs, self.session, cmd, args)
            except KeyboardInterrupt:
                exit()
            except Exception:
                # if exception happens close connections and restart sesseion
                try:self.session.data.close()
                except:pass
                try:self.session.conn.close()
                except:pass
                self.session._log_file.close()
                self.session = Session()

    def __del__(self):
        # on exit attempt to close sockets and save the file system
        try:self.session.conn.close()
        except:pass
        try:self.socket.close()
        except:pass
        try:self.fs.save()
        except:pass
