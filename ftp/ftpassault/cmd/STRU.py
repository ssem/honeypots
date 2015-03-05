class Cmd():
    def __call__(self, fs, ftp, args):
        ftp.conn_send_and_log('We only support file structure, sorry.\r\n')
