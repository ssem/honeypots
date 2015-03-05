class Cmd():
    def __call__(self, fs, ftp, args):
        ftp.username = None
        ftp.password = None
        ftp.authenitcated = False
        ftp.data = None
        ftp.cwd = '/'
