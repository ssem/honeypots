import os

class Cmd():
    def __call__(self, fs, ftp, args):
        if ftp.data is not None:
            ftp.conn_send_and_log('150 Opening BINARY mode data connection for File.\r\n')
            path = os.path.normpath(args)
            if path == '.':
                fullpath = ftp.cwd
            elif path.startswith('~'):
                fullpath = os.path.join('/', path.lstrip('~'))
            elif not path.startswith('/'):
                fullpath = os.path.join(ftp.cwd, path)
            else:
                fullpath = path
            content = fs.getfile(fullpath).content
            while True:
                if len(content) < 1:
                    break
                ftp.data_send_and_log(content[:1024])
                content = content[1024:]
            ftp.data.close()
            ftp.data = None
            ftp.conn_send_and_log('226 Transfer complete.\r\n')
        else:
            ftp.conn_send_and_log('550 Port command unsuccessful.\r\n')


