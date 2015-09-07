import os
import random
from ftpassault.config import Config

class Cmd():
    def __call__(self, fs, ftp, args):
        if ftp.data is not None:
            path = os.path.normpath(args)
            fullpath = path
            if path == '.':
                fullpath = ftp.cwd
            elif path.startswith('~'):
                fullpath = os.path.join('/', path.lstrip('~'))
            elif not path.startswith('/'):
                fullpath = os.path.join(ftp.cwd, path)
            if fs.direxists(os.path.dirname(fullpath)) and not fs.direxists(fullpath):
                if fs.fileexists(fullpath):
                    fs.rm(fullpath)
                ftp.send('150 ok to send data.\r\n')
                content = ''
                while True:
                    data = ftp.data.recv(1024)
                    if not data:
                        break
                    content += data.replace('\r\n', '\n')
                config = Config()
                dlname = '%s_%s' % (fullpath.lstrip('/'), random.randint(0,10000000))
                dlpath = os.path.join(config.download_path, dlname)
                f = open(dlpath, 'wb')
                f.write(content)
                f.close()
                fs.mkfile(fullpath, 1000, ftp.username, 1000, ftp.username,
                    len(content), 33188, content=content)
                ftp.data.close()
                ftp.data = None
                ftp.send('226 Transfer complete.\r\n')
            else:
                ftp.send('554 Could not create file.\r\n')
        else:
            ftp.send('550 Port command unsuccessful.\r\n')
