class Cmd():
    def __call__(self, fs, ftp, args):
        ftp.conn_send_and_log('No proxy connection..\r\n')
        ftp.conn_send_and_log('Mode: stream; Type: binary: Form: non-print; Structure: file\r\n')
        ftp.conn_send_and_log('Verbose: on; Bell: off; Propting: on; Globbing on\r\n')
        ftp.conn_send_and_log('Store unique: off; Receive unique: off\r\n')
        ftp.conn_send_and_log('Case: off; CR stripping: on\r\n')
        ftp.conn_send_and_log('Ntrans: off\r\n')
        ftp.conn_send_and_log('Nmap: off\r\n')
        ftp.conn_send_and_log('Hash mark printing: off; Use of PORT cmds: on')
        ftp.conn_send_and_log('Tick counter printing: off\r\n')
