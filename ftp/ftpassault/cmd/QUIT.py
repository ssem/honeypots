class Cmd():
    def __call__(self, fs, ftp, args):
        ftp.disconnect = True
