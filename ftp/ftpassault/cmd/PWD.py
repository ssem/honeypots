class Cmd():
    def __call__(self, fs, ftp, args):
        ftp.send('257 "%s"\r\n' % ftp.cwd)
