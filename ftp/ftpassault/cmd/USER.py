class Cmd():
    def __call__(self, fs, ftp, args):
        ftp.username = args
        ftp.conn_send_and_log('331 Please specify the password.\r\n')
