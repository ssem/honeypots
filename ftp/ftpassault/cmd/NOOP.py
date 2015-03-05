class Cmd():
    def __call__(self, fs, ftp, args):
        ftp.conn_send_and_log('200 OK\r\n')
