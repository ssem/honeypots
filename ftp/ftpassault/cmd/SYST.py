
class Cmd():
    def __call__(self, fs, ftp, args):
        ftp.send('215 UNIX Type: L8\r\n')
