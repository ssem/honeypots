import os

class Cmd():
    def __call__(self, fs, ftp, args):
        path = os.path.normpath(args)
        if path == '.':
            fullpath = ftp.cwd
        elif path.startswith('~'):
            fullpath = os.path.join('/', path.lstrip('~'))
        elif not path.startswith('/'):
            fullpath = os.path.join(ftp.cwd, path)
        else:
            fullpath = args
        if fs.fileexists(fullpath):
            result = fs.rm(fullpath)
            if result is None:
                ftp.send('250 Delete operation successful.\r\n')
                return
        ftp.send('550 Delete operation failed.\r\n')
