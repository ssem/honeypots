import os

class Cmd():
    def __call__(self, fs, ftp, args):
        ftp.cwd = os.path.dirname(ftp.cwd)
        ftp.send('250 Directory successfully changed.\r\n')
