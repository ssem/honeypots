class Cmd():
    def __call__(self, fs, ftp, args):
        ftp.send('502 not implemented.\r\n')
