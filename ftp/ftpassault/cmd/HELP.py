class Cmd():
    def __call__(self, fs, ftp, args):
        ftp.send('214 Help ok.\r\n')
