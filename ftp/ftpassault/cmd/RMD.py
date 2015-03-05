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
        if fs.direxists(fullpath):
            result = fs.rm(fullpath)
            if result is None:
                ftp.conn_send_and_log('250 Remove directory operation successful.\r\n')
                return
        ftp.conn_send_and_log('550 Remove directory operation failed.\r\n')
