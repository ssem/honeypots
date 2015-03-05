import os

class Cmd():
    def __call__(self, fs, ftp, args):
        if ftp.rnfr is not None:
            path = os.path.normpath(args)
            if path == '.':
                path = ftp.cwd
            result = fs.mv(ftp.rnfr, path)
            if result is None:
                ftp.conn_send_and_log('250 Rename successful.\r\n')
                return
        ftp.conn_send_and_log('550 Rename failed.\r\n')
