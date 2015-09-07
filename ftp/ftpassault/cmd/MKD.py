import os

class Cmd():
    def __call__(self, fs, ftp, args):
        fullpath = os.path.normpath(args)
        if fullpath == '.':
            fullpath = ftp.cwd
        result = fs.mkdir(fullpath, 1000, ftp.username, 1000, ftp.username,
            4096, 16877)
        if result is None:
            ftp.send('257 "%s" create\r\n' % path)
        else:
            ftp.send('550 Create directory operation failed.\r\n')
