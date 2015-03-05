class Cmd():
    def __call__(self, fs, ftp, args):
        ftp.conn_send_and_log('Using binary mode to transfer files.\r\n')
