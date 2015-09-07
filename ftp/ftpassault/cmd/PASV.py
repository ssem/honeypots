import socket

class Cmd():
    def __call__(self, fs, ftp, args):
        pasv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        pasv_sock.bind(('', 0))
        pasv_sock.listen(1)
        ip, port = pasv_sock.getsockname()
        ftp.send('227 Entering Passive Mode (%s, %u, %u).\r\n' %
            (','.join(ip.split('.')), port>>8&0xFF, port&0xFF))
        ftp.data, addr = pasv_sock.accept()
