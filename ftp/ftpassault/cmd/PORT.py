import socket

class Cmd():
    def __call__(self, fs, ftp, args):
        args = args.split(',')
        ip = '.'.join(args[:4])
        port = (int(args[4])<<8) + int(args[5])
        ftp.data = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ftp.data.connect((ip, port))
        ftp.conn_send_and_log('200 Port command successful. Consider using PASV.\r\n')
