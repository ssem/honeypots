import os

class Cmd():
    def __call__(self, fs, ftp, args):
        if ftp.data is not None:
            ftp.conn_send_and_log('150 Here comes the directory listing.\r\n')
            path = os.path.normpath(args)
            if path == '.':
                fullpath = ftp.cwd
            elif path.startswith('~'):
                fullpath = os.path.join('/', path.lstrip('~'))
            elif not path.startswith('/'):
                fullpath = os.path.join(ftp.cwd, path)
            else:
                fullpath = path
            files = fs.listdir(fullpath)
            if files is not None:
                for f in files:
                    fo = files[f]
                    ftp.data_send_and_log('{}{} {:>4} {:>4} {:>8} {:>12} {} {}\r\n'.format(
                        fo.file_type, fo.unix_mode, fo.hardlinks, fo.uid, fo.gid,
                        fo.size, fo.unix_time, fo.name))
            ftp.data.close()
            ftp.data = None
            ftp.conn_send_and_log('226 Directory send OK.\r\n')
        else:
            ftp.conn_send_and_log('550 Port command unsuccessful.\r\n')
