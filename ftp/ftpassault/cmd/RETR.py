import os

class Cmd():
    def __call__(self, fs, ftp, args):
        if ftp.data is not None:
            ftp.send('150 Opening BINARY mode data connection for File.\r\n')
            path = os.path.normpath(args)
            if path == '.':
                fullpath = ftp.cwd
            elif path.startswith('~'):
                fullpath = os.path.join('/', path.lstrip('~'))
            elif not path.startswith('/'):
                fullpath = os.path.join(ftp.cwd, path)
            else:
                fullpath = path
            if fs.fileexists(fullpath):
                fake_file = fs.getfile(fullpath)
                try:content = str(os.urandom(int(fake_file.size)))
                except:content = ""
                while True:
                    if len(content) < 1:
                        break
                    ftp.send_data(content[:1024])
                    content = content[1024:]
                ftp.data.close()
                ftp.data = None
                ftp.send('226 Transfer complete.\r\n')
            else:
                ftp.data.close()
                ftp.data = None
                ftp.send('550 Failed to open file.\r\n')
        else:
            ftp.send('550 Port command unsuccessful.\r\n')
