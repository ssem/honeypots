class Cmd():
    def __call__(self, fs, ftp, args):
        ftp.send('No proxy connection..\r\n')
        ftp.send('Mode: stream; Type: binary: Form: non-print; Structure: file\r\n')
        ftp.send('Verbose: on; Bell: off; Propting: on; Globbing on\r\n')
        ftp.send('Store unique: off; Receive unique: off\r\n')
        ftp.send('Case: off; CR stripping: on\r\n')
        ftp.send('Ntrans: off\r\n')
        ftp.send('Nmap: off\r\n')
        ftp.send('Hash mark printing: off; Use of PORT cmds: on')
        ftp.send('Tick counter printing: off\r\n')
