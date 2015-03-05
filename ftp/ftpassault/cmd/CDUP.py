import os

class Cmd():
    def __call__(self, fs, ftp, args):
        ftp.cwd = os.path.dirname(ftp.cwd)
        ftp.conn_send_and_log('250 Directory successfully changed.\r\n')
