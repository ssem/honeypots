class Cmd():
    def __call__(self, fs, ftp, args):
        ftp.send('We only support stream mode, sorry.\r\n')
