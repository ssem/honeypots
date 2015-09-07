class Cmd():
    def __call__(self, fs, ftp, args):
        ftp.username = args
        ftp.send('331 Please specify the password.\r\n')
