import os

class Cmd():
    def __call__(self, fs, ftp, args):
        ftp.rnfr = os.path.normpath(args)
        if ftp.rnfr == '.':
            ftp.rnfr = ftp.cwd
        ftp.send('350 Ready for RNTO.\r\n')
