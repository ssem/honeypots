import os
import time
import socket
from ftpassault.config import Config

# object passed to each command
class Session():
    def __init__(self, timeout=120):
        self.disconnect = False     # switch to true if you want the server to disconnect
        self.username = None        # username supplied by client
        self.password = None        # password supplied by client
        self.authenticated = False  # is user authenticated
        self.conn = None            # ftp connection socket
        self.addr = None            # ftp connection addr
        self.data = None            # ftp data socket
        self.rnfr = None            # rename from
        self.cwd = '/'              # current working directory
        self._log_file = None       # file object for logging
        socket.setdefaulttimeout(timeout)
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def bind(self, addr):
        return self._socket.bind(addr)

    def listen(self, backlog):
        try:return self._socket.listen(backlog)
        except socket.error as e:
            if e.errno == 13:
                exit("Ports below 1024 must run as root")
            raise e

    def accept(self):
        while not self.conn:
            try:self.conn, self.addr = self._socket.accept()
            except socket.error:self.conn = None
        self._open_log_file(self.addr)

    def send(self, message):
        '''sends data to connection socket and writes data to log file'''
        timestamp = time.strftime('%b-%d-%H-%M-%S', time.gmtime())
        try:self._log_file.write('s:%s:%s' % (timestamp, message))
        except: print "[-] Error logging"
        print "[+] CONN", message.rstrip("\r\n")
        self.conn.send(message)

    def recv(self, size):
        '''returns data from connection socket and writes recieved data to log file'''
        message = self.conn.recv(size)
        timestamp = time.strftime('%b-%d-%H-%M-%S', time.gmtime())
        try:self._log_file.write('c:%s:%s' % (timestamp, message))
        except: print "[-] Error logging"
        return message

    def close(self):
        try:self.conn.close()
        except:pass
        try:self.data.close()
        except:pass
        self.disconnect = False
        self.username = None
        self.password = None
        self.authenticated = False
        self.conn = None
        self.addr = None
        self.data = None
        self.rnfr = None
        self.cwd = '/'
        self._log_file = None
        try:self._log_file.close()
        except:pass

    def _open_log_file(self, addr):
        conf = Config()
        timestamp = time.strftime('%b_%d_%H:%M', time.gmtime())
        logpath = os.path.join(conf.log_path, '%s_%s' % (addr[0],timestamp))
        if not os.path.isdir(os.path.dirname(logpath)):
            os.makedirs(os.path.dirname(logpath))
        self._log_file = open(logpath, 'w+')

    def send_data(self, message):
        '''sends data to data socket and writes data to log file'''
        #try:self._log_file.write('s:%s' % message)
        #except:pass
        self.data.send(message)

    def recv_data(self, size):
        '''returns data from data socket and writes recieved data to log file'''
        message = self.data.recv(size)
        #try:self._log_file.write('c:%s' % message)
        #except:pass
        return message

    # for debugging perposes when writing commands
    def __str__(self):
        r = 'CLASS ATTRIBUTES\n'
        r += 'disconnect: %s\n' % self.disconnect
        r += 'username: %s\n' % self.username
        r += 'password: %s\n' % self.password
        r += 'authenticated: %s\n' % self.authenticated
        r += 'mode: %s\n' % self.mode
        r += 'conn: %s\n' % self.conn
        r += 'data: %s\n' % self.data
        r += 'rnfr: %s\n' % self.rnfr
        r += 'cwd: %s\n' % self.cwd
