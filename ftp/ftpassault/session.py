import os
import time
from ftpassault.config import Config

# object passed to each command
class Session():
    def __init__(self):
        self.disconnect = False     # switch to true if you want the server to disconnect
        self.username = None        # username supplied by client
        self.password = None        # password supplied by client
        self.authenticated = False  # is user authenticated
        self.conn = None            # ftp connection socket
        self.data = None            # ftp data socket
        self.rnfr = None            # rename from
        self.cwd = '/'              # current working directory
        self._log_file = None       # file object for logging

    def open_log_file(self, addr):
        '''should only be used by server'''
        conf = Config()
        timestamp = time.strftime('%b_%d_%H:%M', time.gmtime())
        logpath = os.path.join(conf.log_path, '%s_%s' % (addr[0],timestamp))
        if not os.path.isdir(os.path.dirname(logpath)):
            os.makedirs(os.path.dirname(logpath))
        self._log_file = open(logpath, 'w+')

    def conn_send_and_log(self, message):
        '''sends data to connection socket and writes data to log file'''
        try:self._log_file.write('s:%s' % message)
        except:pass
        print "[+] CONN", message.rstrip("\r\n")
        self.conn.send(message)

    def conn_recv_and_log(self, size):
        '''returns data from connection socket and writes recieved data to log file'''
        message = self.conn.recv(size)
        try:self._log_file.write('c:%s' % message)
        except:pass
        return message

    def data_send_and_log(self, message):
        '''sends data to data socket and writes data to log file'''
        try:self._log_file.write('s:%s' % message)
        except:pass
        print "[+] DATA", message.rstrip("\r\n")
        self.data.send(message)

    def data_recv_and_log(self, size):
        '''returns data from data socket and writes recieved data to log file'''
        message = self.data.recv(size)
        try:self._log_file.write('c:%s' % message)
        except:pass
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
