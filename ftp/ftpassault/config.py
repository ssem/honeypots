import os
import ConfigParser


class Config():
    def __init__(self):
        # set all attributes to default config options
        self.ftp_port = '2121'
        self.hostname = 'workhorse'
        self.log_path = 'log'
        self.download_path = 'download'
        self.download_limit_size = '2147483648'
        self.file_system_path = 'conf/file_system.pickle'
        self.password_path = 'conf/password.db'
        self.ftp_version_string = '200 (vsFTPd 3.0.2)'
        self._try_loading_conf_file()

    def _try_loading_conf_file(self):
        conf = ConfigParser.ConfigParser()
        # looks in these 3 locations for a config file
        for f in ['conf/ftpassault.conf',
                  '/etc/ftpassault.conf',
                  '/etc/ftpassault/ftpassault.conf']:
            # if conifg is found change default attributes to match config file
            if os.path.exists(f):
                conf.read(f)
                if conf.has_option('honeypot', 'ftp_port'):
                    self.ftp_port = conf.get('honeypot', 'ftp_port')
                if conf.has_option('honeypot', 'hostname'):
                    self.hostname = conf.get('honeypot', 'hostname')
                if conf.has_option('honeypot', 'log_path'):
                    self.log_path = conf.get('honeypot', 'log_path')
                if conf.has_option('honeypot', 'download_path'):
                    self.download_path = conf.get('honeypot', 'download_path')
                if conf.has_option('honeypot', 'download_limit_size'):
                    self.download_limit_size = conf.get('honeypot', 'download_limit_size')
                if conf.has_option('honeypot', 'file_system_path'):
                    self.file_system_path = conf.get('honeypot', 'file_system_path')
                if conf.has_option('honeypot', 'password_path'):
                    self.password_path = conf.get('honeypot', 'password_path')
                if conf.has_option('honeypot', 'ftp_version_string'):
                    self.ftp_version_string = conf.get('honeypot', 'ftp_version_string')
