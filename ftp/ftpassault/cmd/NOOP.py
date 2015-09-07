class Cmd():
    def __call__(self, fs, ftp, args):
        ftp.send('200 OK\r\n')
