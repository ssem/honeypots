import os

class Cmd():
    def __call__(self, fs, ftp, args):
        path = os.path.normpath(args)
        if path == '.':
            pass
        elif path == '..':
            ftp.cwd = os.path.dirname(ftp.cwd)
        else:
            ftp.cwd = os.path.join(ftp.cwd, path)
        ftp.send('250 Directory successfully changed.\r\n')
