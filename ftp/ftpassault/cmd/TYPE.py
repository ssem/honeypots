class Cmd():
    def __call__(self, fs, ftp, args):
        ftp.send('Using binary mode to transfer files.\r\n')
