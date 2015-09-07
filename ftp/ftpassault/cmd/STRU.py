class Cmd():
    def __call__(self, fs, ftp, args):
        ftp.send('We only support file structure, sorry.\r\n')
