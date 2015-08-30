import os
import pwd
import time
import pickle
import argparse
import readline
import datetime

# object represents fake file
class File():
    def __init__(self, name, file_type, hardlinks, uid, suid, gid, sgid, size, mode, ctime, content):
        self.name = name
        self.file_type = file_type
        self.hardlinks = hardlinks
        self.uid = uid
        self.string_uid = suid
        self.gid = gid
        self.string_gid = sgid
        self.size = size
        self.mode = mode
        self.ctime = ctime
        self.content = content

    @property
    def unix_mode(self):
        '''converts from bin to char repr'''
        mode = str(bin(self.mode)[-9:])
        unix_mode = ''
        permissions = 'rwxrwxrwx'
        for x in xrange(9):
            if mode[x] == '1':
                unix_mode += permissions[x]
            else:
                unix_mode += '-'
        return unix_mode

    @property
    def unix_time(self):
        '''converts from float to char repr'''
        timestamp = datetime.datetime.fromtimestamp(self.ctime)
        return timestamp.strftime('%b %d %H:%M')

    def __str__(self):
        '''for debugging perposes'''
        r = 'CLASS ATTRIBUTES\n'
        r += 'name: %s\n' % self.name
        r += 'file_type: %s\n' % self.file_type
        r += 'hardlinks: %s\n' % self.hardlinks
        r += 'uid: %s\n' % self.uid
        r += 'string_uid: %\n' % self.string_uid
        r += 'gid: %s\n' % self.gid
        r += 'string_gid: %\n' % self.string_gid
        r += 'size: %s\n' % self.size
        r += 'mode: %s\n' % self.mode
        r += 'unix_mode: %s\n' % self.unix_mode
        r += 'ctime: %s\n' % self.ctime
        r += 'unix_time: %s\n' % self.unix_time
        r += 'content: %s\n' % self.content
        return r


# object represents fake file system
class File_System():
    def __init__(self, fs_path=None):
        self.fs_path = fs_path
        # load fake file sysem from disk
        try:self.fs = pickle.load(open(fs_path, 'rb'))
        except:
            print '[-] Can not load file system: %s' % fs_path
            self.fs = {'/': {'files': {}, 'stats': None}}

    def mkdir(self, fullpath, uid, suid, gid, sgid, size, mode, hardlinks=2, ctime=time.time(), content=''):
        '''creates a fake dir'''
        dirname = os.path.dirname(fullpath)
        basename = os.path.basename(fullpath)
        # return error if file exists
        if self.exists(fullpath):
            return "'%s': File exists" % fullpath
        # return error if dir exists
        elif not self.direxists(dirname):
            return "'%s': No such file or directory" % fullpath
        # create dir and add to file system
        try:
            directory = File(basename, 'd', hardlinks, uid, suid, gid, sgid, size, mode, ctime, content)
            self.fs[fullpath] = {'stats':directory, 'files':{}}
        except Exception as e:
            # this should not happen print error to screen and fail silently
            print 'mkdir: %s' % e
        # mkdir was successful return None
        return None

    def mkfile(self, fullpath, uid, suid, gid, sgid, size, mode, hardlinks=1, ctime=time.time(), content=''):
        '''creates a fake file'''
        dirname = os.path.dirname(fullpath)
        basename = os.path.basename(fullpath)
        # return error if file exists
        if self.exists(fullpath):
            return "'%s': File exists" % fullpath
        # return error if invalid path
        if not self.direxists(dirname):
            return "'%s': No such file or directory" % fullpath
        # create file and add to file system
        try:
            myfile = File(basename, '-', hardlinks, uid, suid, gid, sgid, size, mode, ctime, content)
            self.fs[dirname]['files'][basename] = myfile
        except Exception as e:
            # this should not happen print error to screen and fail silently
            print 'mkfile: %s' % e
        # mkfile was successful return None
        return None

    def chlink(self, fullpath, hardlinks):
        '''modifies hardlink count on fake file'''
        # return error if file doesn't exist
        if not self.fileexists(fullpath):
            return "'%s': No such file or directory" % fullpath
        dirname = os.path.dirname(fullpath)
        basename = os.path.basename(fullpath)
        try:
            # check if fullpath is dir
            if self.direxists(fullpath):
                obj = self.fs[fullpath]['stats']
            # check if fullpath is file
            elif self.fileexists(fullpath):
                obj = self.fs[dirname]['files'][basename]
            # set objects hardlinks
            obj.hardlinks = hardlinks
        except Exception as e:
            # this should not happend print error to screen and fail silently
            print 'chlink: %s' % e
        # chlink was successful return None
        return None


    def chmod(self, fullpath, mode):
        '''modifies the mode on fake file'''
        # return error if file doesn't exist
        if not self.fileexists(fullpath):
            return "'%s': No such file or directory" % fullpath
        dirname = os.path.dirname(fullpath)
        basename = os.path.basename(fullpath)
        try:
            # check if fullpath is dir
            if self.direxists(fullpath):
                obj = self.fs[fullpath]['stats']
            # check if fullpath is file
            elif self.fileexists(fullpath):
                obj = self.fs[dirname]['files'][basename]
            # try setting objects mod
            obj.mode = mode
        except Exception as e:
            # this should not happen print error to screen and fail silently
            print 'chmod: %s' % e
        # chmod was successfull return None
        return None

    def chown(self, fullpath, suid, sgid, uid=1000, gid=1000):
        '''modifies the ownership of fake file'''
        # return error if file doesn't exist
        if not self.fileexists(fullpath):
            return "'%s': No such file or directory" % fullpath
        dirname = os.path.dirname(fullpath)
        basename = os.path.basename(fullpath)
        try:
            # check if fullpath is dir
            if self.direxists(fullpath):
                obj = self.fs[fullpath]['stats']
            # check if fullpath is file
            elif self.fileexists(fullpath):
                obj = self.fs[dirname]['files'][basename]
            # try setting objects suid, sgid, uid, gid
            obj.string_uid = suid
            obj.string_gid = sgid
            obj.uid = uid
            obj.gid = gid
        except Exception as e:
            # this should not happen print error to screen and fail silently
            print 'chown: %s' % e
        # chown was successful return None
        return None

    def chtime(self, fullpath, ctime):
        '''modifies the time of fake file'''
        # return error if path doesn't exist
        if not self.exists(fullpath):
            return "'%s': No such file or directory" % fullpath
        dirname = os.path.dirname(fullpath)
        basename = os.path.basename(fullpath)
        try:
            # check if fullpath is dir
            if self.direxists(fullpath):
                obj = self.fs[fullpath]['stats']
            # check if fullpath is file
            elif self.fileexists(fullpath):
                obj = self.fs[dirname]['files'][basename]
            # try setting objects ctime
            obj.ctime = float(ctime)
        except Exception as e:
            # this should not happen print error to screen and fail silently
            print 'chtime: %s' % e
        # chtime was succesful return None
        return None

    def chsize(self, fullpath, size):
        '''modifies the size of fake file'''
        # return error if path doesn't exist
        if not self.exists(fullpath):
            return "'%s': No such file or directory" % fullpath
        dirname = os.path.dirname(fullpath)
        basename = os.path.basename(fullpath)
        try:
            # check if fullpath is dir
            if self.direxists(fullpath):
                obj = self.fs[fullpath]['stats']
            # check if fullpath is file
            elif self.fileexists(fullpath):
                obj = self.fs[dirname]['files'][basename]
            # try setting objects size
            obj.size = int(size)
        except Exception as e:
            # this should not happen print error to screen and fail silently
            print 'chsize: %s' % e
        return None

    def mv(self, fullpath_src, fullpath_dst):
        '''move fake file'''
        sd = os.path.dirname(fullpath_src)
        sb = os.path.basename(fullpath_src)
        dd = os.path.dirname(fullpath_dst)
        db = os.path.basename(fullpath_dst)
        if not self.exists(fullpath_src):
            return "'%s': No such file or directory" % fullpath_src
        elif fullpath_src in self.fs and fullpath_dst in self.fs or \
        fullpath_src in self.fs and not self.exists(fullpath_dst):
            self.fs[dd] = self.fs[sd]
            nf = {}
            for path in self.fs:
                if path.startswith(fullpath_src):
                    nf[path.replace(fullpath_src, fullpath_dst)] = self.fs[path]
            self.rm(fullpath_dst)
            self.fs.update(nf)
            self.rm(fullpath_src)
        elif self.fileexists(fullpath_src) and self.fileexists(fullpath_dst) or \
        self.fileexists(fullpath_src) and not self.exists(fullpath_dst):
            self.fs[dd]['files'][db] = self.fs[sd]['files'][sb]
            del self.fs[sd]['files'][sb]
        else:
            return "cannot overwrite '%s' with '%s'" % (fullpath_dst, fullpath_src)

    def rm(self, fullpath):
        '''remove fake file'''
        dirname = os.path.dirname(fullpath)
        basename = os.path.basename(fullpath)
        if fullpath in self.fs:
            remove = {fullpath:''}
            for path in self.fs:
                if path.startswith(fullpath + '/'):
                    remove[path] = ''
            for path in remove:
                del self.fs[path]
            return None
        elif dirname in self.fs:
            if basename in self.fs[dirname]['files']:
                del self.fs[dirname]['files'][basename]
                return None
        return "'%s': No such file or directory" % fullpath

    def listdir(self, fullpath):
        '''list directory of fake file system'''
        if fullpath in self.fs:
            files = {}
            files.update(self.fs[fullpath]['files'])
            for path in self.fs:
                dirname = os.path.dirname(path)
                if fullpath != path and dirname == fullpath:
                    files.update({os.path.basename(path):self.fs[path]['stats']})
            return files
        return None

    def getfile(self, fullpath):
        '''retrieve fake file object'''
        dirname = os.path.dirname(fullpath)
        basename = os.path.basename(fullpath)
        return self.listdir(dirname)[basename]

    def exists(self, fullpath):
        '''check if path exists in fake file system'''
        dirname = os.path.dirname(fullpath)
        basename = os.path.basename(fullpath)
        if fullpath in self.fs:
            return True
        elif dirname in self.fs:
            if basename in self.fs[dirname]['files']:
                return True
        return False

    def fileexists(self, fullpath):
        '''check if file exists in fake file system'''
        if self.exists(fullpath) and not self.direxists(fullpath):
            return True
        return False

    def direxists(self, fullpath):
        '''check if directory exists in fake file system'''
        if fullpath in self.fs:
            return True
        return False

    def save(self):
        '''save fake file system to disk'''
        f = open(self.fs_path, 'wb')
        pickle.dump(self.fs, f)
        f.close()


class Shell():
    def __init__(self, fs_path):
        self.fs = File_System(fs_path)
        self.cwd = '/'
        self.parser = argparse.ArgumentParser()

    def mkdir(self, args):
        parser = argparse.ArgumentParser()
        parser.add_argument('directory', nargs='*')
        args = parser.parse_args(args)
        for dirname in args.directory:
            if dirname.startswith('/'):
                fullpath = dirname
            else:
                fullpath = os.path.join(self.cwd, dirname)
            result = self.fs.mkdir(fullpath, 1000, 'root', 1000, 'root', 4096, 16877)
            if result is not None:
                print result

    def touch(self, args):
        parser = argparse.ArgumentParser()
        parser.add_argument('file', nargs='*')
        args = parser.parse_args(args)
        for filename in args.file:
            if filename.startswith('/'):
                fullpath = filename
            else:
                fullpath = os.path.join(self.cwd, filename)
            result = self.fs.mkfile(fullpath, 1000, 'root', 1000, 'root', 0, 33188)
            if result is not None:
                print result

    def chlink(self, args):
        parser = argparse.ArgumentParser()
        parser.add_argument('hardlinks')
        parser.add_argument('file')
        args = parser.parse_args(args)
        if args.file.startswith('/'):
            fullpath = args.file
        else:
            fullpath = os.path.join(self.cwd, args.file)
        result = self.fs.chlink(fullpath, int(args.hardlinks))
        if result is not None:
            print result

    def chmod(self, args):
        parser = argparse.ArgumentParser()
        parser.add_argument('mode')
        parser.add_argument('file')
        args = parser.parse_args(args)
        if args.file.startswith('/'):
            fullpath = args.file
        else:
            fullpath = os.path.join(self.cwd, args.file)
        if args.mode == '+x':
            args.mode = 33261
        elif args.mode == '-x':
            args.mode = 33188
        result = self.fs.chmod(fullpath, int(args.mode))
        if result is not None:
            print result

    def chown(self, args):
        parser = argparse.ArgumentParser()
        parser.add_argument('uid')
        parser.add_argument('gid')
        parser.add_argument('-n', nargs=2, help='set uid, gid numbers')
        parser.add_argument('file')
        args = parser.parse_args(args)
        if args.file.startswith('/'):
            fullpath = args.file
        else:
            fullpath = os.path.join(self.cwd, args.file)
        if args.n:
            result = self.fs.chown(fullpath, args.uid, args.gid, args.n[0], args.n[1])
        else:
            result = self.fs.chown(fullpath, args.uid, args.gid)
        if result is not None:
            print result

    def chtime(self, args):
        parser = argparse.ArgumentParser()
        parser.add_argument('time')
        parser.add_argument('file')
        args = parser.parse_args(args)
        if args.file.startswith('/'):
            fullpath = args.file
        else:
            fullpath = os.path.join(self.cwd, args.file)
        result = self.fs.chtime(fullpath, args.time)
        if result is not None:
            print result

    def chsize(self, args):
        parser = argparse.ArgumentParser()
        parser.add_argument('size')
        parser.add_argument('file')
        args = parser.parse_args(args)
        if args.file.startswith('/'):
            fullpath = args.file
        else:
            fullpath = os.path.join(self.cwd, args.file)
        result = self.fs.chsize(fullpath, args.size)
        if result is not None:
            print result

    def cd(self, args):
        parser = argparse.ArgumentParser()
        parser.add_argument('path', nargs='*')
        args = parser.parse_args(args)
        if not args.path or args.path[0] == '~' or args.path[0] == '/':
            self.cwd = '/'
            return
        if args.path[0] == '..':
            self.cwd = os.path.dirname(self.cwd)
            return
        if args.path[0].startswith('/'):
            fullpath = args.path[0].rstrip('/')
        else:
            fullpath = os.path.join(self.cwd, args.path[0]).rstrip('/')
        if self.fs.direxists(fullpath):
            self.cwd = fullpath
        else:
            print 'cd: %s: Not a directory' % fullpath

    def ls(self, args):
        parser = argparse.ArgumentParser()
        parser.add_argument('path', nargs='*')
        parser.add_argument('-l', action='store_true',
            help='use a long listing format')
        args = parser.parse_args(args)
        if not args.path:
            args.path.append(self.cwd)
        elif args.path == '~':
            args.path.append('/')
        for path in args.path:
            if path.startswith('/'):
                fullpath = path
            else:
                fullpath = os.path.join(self.cwd, path)
            files = self.fs.listdir(fullpath)
            if files is None:
                print 'ls: cannot access %s: No such file or directory' % path
                continue
            result = ''
            for filename in files:
                f = files[filename]
                if f.file_type == 'd':
                    filename = '\033[94m%s\033[0m' % filename
                elif bin(f.mode)[-7] == '1':
                    filename = '\033[92m%s\033[0m' % filename
                if args.l:
                    print '{}{:9} {:2} {} {} {:8} {:10} {}'.format(
                        f.file_type, f.unix_mode, f.hardlinks,
                        f.string_uid, f.string_gid, f.size, f.unix_time, filename)
                else:
                    result += '%s  ' % filename
            if result != '':
                print result

    def mv(self, args):
        parser = argparse.ArgumentParser()
        parser.add_argument('src')
        parser.add_argument('dst')
        args = parser.parse_args(args)
        if args.src.startswith('/'):
            src_fullpath = args.src
        else:
            src_fullpath = os.path.join(self.cwd, args.src)
        if args.dst.startswith('/'):
            dst_fullpath = args.dst
        else:
            dst_fullpath = os.path.join(self.cwd, args.dst)
        result = self.fs.mv(src_fullpath, dst_fullpath)
        if result is not None:
            print result

    def rm(self, args):
        parser = argparse.ArgumentParser()
        parser.add_argument('path', nargs='*')
        parser.add_argument('-r', '--recursive', action='store_true',
            help='remove directories and their contents recursively')
        args = parser.parse_args(args)
        for path in args.path:
            if path.startswith('/'):
                fullpath = path.rstrip('/')
            else:
                fullpath = os.path.join(self.cwd, path)
            if self.fs.exists(fullpath):
                if self.fs.direxists(fullpath):
                    if args.recursive:
                        result = self.fs.rm(fullpath)
                        if result is not None:
                            print result
                    else:
                        print "rm: cannot remove '%s' Is a directory" % path
                else:
                    result = self.fs.rm(fullpath)
                    if result is not None:
                        print result
            else:
                print "rm: cannot remove '%s' No such file or directory" % path

    def save_file_system(self):
        self.fs.save()

    def help(self):
        print 'mkdir\t\tcreate a directory'
        print 'touch\t\tcreate a file'
        print 'chlink\t\tchange hardlink number of file'
        print 'chmod\t\tchange permissions of file'
        print 'chown\t\tchange ownership of file'
        print 'chtime\t\tchange ctime of file'
        print 'chsize\t\tchange size of file'
        print 'cd\t\tchange current working directory'
        print 'ls\t\tlist files'
        print 'mv\t\tmove file'
        print 'rm\t\tremove file'
        print 'clear\t\tclear screen'
        print 'save\t\tsave file system to disk'
        print 'help\t\tprint this help menu'
        print 'file_system\tprint file system to screen'
        print 'exit\t\texit shell'

    def shell(self):
        readline.parse_and_bind('tab: complete')
        readline.set_completer(complete)
        while True:
            try:
                global CMDS
                CMDS = ['mkdir', 'touch', 'chlink', 'chmod', 'chown',
                        'mv', 'cd', 'ls', 'rm', 'file_system', 'save',
                        'exit', 'help', 'chtime', 'chsize']
                try:
                    for filename in self.fs.listdir(self.cwd):
                        CMDS.append(filename)
                except:pass
                args = raw_input('%s $ ' % self.cwd).lstrip(' ').split()
                if args[0] == 'mkdir':
                    self.mkdir(args[1:])
                elif args[0] == 'touch':
                    self.touch(args[1:])
                elif args[0] == 'chlink':
                    self.chlink(args[1:])
                elif args[0] == 'chmod':
                    self.chmod(args[1:])
                elif args[0] == 'chown':
                    self.chown(args[1:])
                elif args[0] == 'chtime':
                    self.chtime(args[1:])
                elif args[0] == 'chsize':
                    self.chsize(args[1:])
                elif args[0] == 'mv':
                    self.mv(args[1:])
                elif args[0] == 'cd':
                    self.cd(args[1:])
                elif args[0] == 'ls':
                    self.ls(args[1:])
                elif args[0] == 'rm':
                    self.rm(args[1:])
                elif args[0] == 'file_system':
                    print self.fs.fs
                elif args[0] == 'clear':
                    os.system('clear')
                elif args[0] == 'save':
                    print 'Progress saved'
                    self.save_file_system()
                elif args[0] == 'help':
                    self.help()
                elif args[0] == 'exit':
                    raise StopIteration
                else:
                    print '%s: command not found' % args[0]
            except StopIteration:
                self.save_file_system()
                return
            #except SystemExit:
            #    pass
            #except Exception as e:
            #    print e


CMDS = []
def complete(text, state):
    global CMDS
    for cmd in CMDS:
        if cmd.startswith(text):
            if not state:
                return cmd
            else:
                state -= 1


class Clone():
    def __init__(self, fs_path):
        self.fs = File_System(fs_path)

    def _create_subdirectories(self, path):
        fake_path = ''
        for dirs in path.split('/')[1:]:
            try:
                fake_path += '/%s' % dirs
                if fake_path == '/':
                    continue
                result = self.fs.mkdir(fake_path,
                    1000, 'root', 1000, 'root', '4096', 16877, 2, time.time())
                if result is not None:
                    print result
                else:
                    print '[+] Added: %s' % fake_path
            except Exception as e: print e
        self.fs.save()

    def clone_dirs(self, prefix, clone_path):
        self._create_subdirectories(prefix)
        size = len(clone_path)
        for root, dirs, files in os.walk(clone_path):
            for d in dirs:
                try:
                    fake_path = os.path.join(prefix, root[size:], d)
                    stats = os.stat(os.path.join(root, d))
                    result = self.fs.mkdir(fake_path,
                        stats.st_uid,
                        pwd.getpwuid(stats.st_uid).pw_name,
                        stats.st_gid,
                        pwd.getpwuid(stats.st_gid).pw_name,
                        stats.st_size,
                        stats.st_mode,
                        stats.st_nlink,
                        stats.st_ctime)
                    if result:
                        print result
                    else:
                        print '[+] Added: %s' % fake_path
                except Exception as e: print e
        self.fs.save()

    def clone_files(self, prefix, clone_path):
        self._create_subdirectories(prefix)
        size = len(clone_path)
        for root, dirs, files in os.walk(clone_path):
            for f in files:
                try:
                    fake_path = os.path.join(prefix, root[size:], f)
                    stats = os.stat(os.path.join(root, f))
                    result = self.fs.mkfile(fake_path,
                        stats.st_uid,
                        pwd.getpwuid(stats.st_uid).pw_name,
                        stats.st_gid,
                        pwd.getpwuid(stats.st_gid).pw_name,
                        stats.st_size,
                        stats.st_mode,
                        stats.st_nlink,
                        stats.st_ctime)
                    if result is not None:
                        print result
                    else:
                        print '[+] Added: %s' % fake_path
                except Exception as e: print e
        self.fs.save()

    def clone_all(self, prefix, clone_path):
        self.clone_dirs(prefix, clone_path)
        self.clone_files(prefix, clone_path)
