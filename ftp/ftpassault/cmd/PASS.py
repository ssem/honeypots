from ftpassault.config import Config

class Cmd():
    def __call__(self, fs, ftp, args):
        conf = Config()
        for line in open(conf.password_path):
            if line.split(':')[0] == ftp.username:
                if line.split(':')[-1].rstrip('\n') ==  args:
                    ftp.password = args
                    ftp.authenticated = True
                    ftp.conn_send_and_log('230 Login successful.\r\n')
                    return
        ftp.disconnect = True
        ftp.conn_send_and_log('530 Login incorrect.\r\n')
