from kippo.core.honeypot import HoneyPotCommand
from twisted.internet import reactor
import os
import random
commands = {}

class command_gcc(HoneyPotCommand):
    RANDOM_DATA = "\x6a\x00\x48\x89\xe5\x48\x83\xe4\xf0\x48\x8b\x7d\x08\x48\x8d\x75\x10\x89\xfa" \
                  "\x83\xc2\x01\xc1\xe2\x03\x48\x01\xf2\x48\x89\xd1\xeb\x04\x48\x83\xc1\x08\x48" \
                  "\x83\x39\x00\x75\xf6\x48\x83\xc1\x08\xe8\x0c\x00\x00\x00\x89\xc7\xe8\xb9\x00" \
                  "\x00\x00\xf4\x90\x90\x90\x90\x55\x48\x89\xe5\x48\x83\xec\x40\x89\x7d\xfc\x48" \
                  "\x89\x75\xf0\x48\x8b\x45\xf0\x48\x8b\x00\x48\x83\xf8\x00\x75\x0c\xb8\x00\x00" \
                  "\x00\x00\x89\xc7\xe8\x8c\x00\x00\x00\x48\x8b\x45\xf0\x48\x8b\x40\x08\x30\xc9" \
                  "\x48\x89\xc7\x88\xc8\xe8\x7e\x00\x00\x00\x89\xc1\x89\x4d\xdc\x48\x8d\x0d\xd8" \
                  "\x01\x00\x00\x48\x89\xcf\x48\x89\x4d\xd0\xe8\x72\x00\x00\x00\x8b\x4d\xdc\x30" \
                  "\xd2\x48\x8d\x3d\xa4\x00\x00\x00\x89\xce\x88\x55\xcf\x48\x89\xc2\x8a\x45\xcf" \
                  "\xe8\x53\x00\x00\x00\x8b\x45\xdc\x88\x05\xc3\x01\x00\x00\x8b\x45\xdc\xc1\xe8" \
                  "\x08\x88\x05\xb8\x01\x00\x00\x8b\x45\xdc\xc1\xe8\x10\x88\x05\xad\x01\x00\x00" \
                  "\x8b\x45\xdc\xc1\xe8\x18\x88\x05\xa2\x01\x00\x00\x48\x8b\x45\xd0\x48\x89\x45" \
                  "\xe0\x48\x8b\x45\xe0\xff\xd0\x8b\x45\xec\x48\x83\xc4\x40\x5d\xc3\xff\x25\x3e" \
                  "\x01\x00\x00\xff\x25\x40\x01\x00\x00\xff\x25\x42\x01\x00\x00\xff\x25\x44\x01" \
                  "\x00\x00\x4c\x8d\x1d\x1d\x01\x00\x00\x41\x53\xff\x25\x0d\x01\x00\x00\x90\x68" \
                  "\x00\x00\x00\x00\xe9\xe6\xff\xff\xff\x68\x0c\x00\x00\x00\xe9\xdc\xff\xff\xff" \
                  "\x68\x1d\x00\x00\x00\xe9\xd2\xff\xff\xff\x68\x2b\x00\x00\x00\xe9\xc8\xff\xff" \
                  "\xff\x01\x00\x00\x00\x1c\x00\x00\x00\x00\x00\x00\x00\x1c\x00\x00\x00\x00\x00" \
                  "\x00\x00\x1c\x00\x00\x00\x02\x00\x00\x00\x00\x0e\x00\x00\x34\x00\x00\x00\x34" \
                  "\x00\x00\x00\xf5\x0e\x00\x00\x00\x00\x00\x00\x34\x00\x00\x00\x03\x00\x00\x00" \
                  "\x0c\x00\x02\x00\x14\x00\x02\x00\x00\x00\x00\x01\x40\x00\x00\x00\x00\x00\x00" \
                  "\x01\x00\x00\x00"

    def start(self):
        output_file = 'a.out'
        if '--version' in self.args:
            self.version(short=True)
            self.exit()
            return
        elif '-v' in self.args:
            self.version(short=False)
            self.exit()
            return
        elif '--help' in self.args:
            self.help()
            self.exit()
            return
        elif '-o' in self.args:
            try:
                output_file = self.args[self.args.index('-o') + 1]
            except:pass
        source_file = ''
        for arg in self.args:
            if '.c' in arg.lower():
                source_file = arg
        if source_file == '':
            self.writeln("gcc: %s: No such file or directory" % source_file)
            self.writeln("gcc: fatal error: no imput files")
            self.writeln("comilation terminated.")
            self.exit()
            return
        self.generate_file(output_file)
        self.exit()
        return

    def generate_file(self, outfile):
        data = ""
        for i in range(random.randint(3, 15)):
            if random.randint(1, 3) == 1:
                data += command_gcc.RANDOM_DATA[::-1]
            else:
                data += command_gcc.RANDOM_DATA
        with open('/tmp/garbage', 'wb') as f: f.write(data)
        outfile = self.fs.resolve_path(outfile, self.honeypot.cwd)
        self.fs.mkfile(outfile, 0, 0, len(data), 33188)
        self.fs.update_realfile(self.fs.getfile(outfile), '/tmp/garbage')
        class segfault_command(HoneyPotCommand):
            def call(self):
                self.write("Segmentation fault\n")
        self.honeypot.commands[outfile] = segfault_command

    def version(self, short=False):
        if short:
            for l in (
                'gcc (Ubuntu 4.8.2-19ubuntu1) 4.8.2',
                'Copyright (C) 2013 Free Software Foundation, Inc.',
                'This is free software; see the source for copying conditions.  There is NO',
                'warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.',
                ):
                self.writeln(l)
        else:
            for l in (
                'Using built-in specs.',
                'COLLECT_GCC=gcc',
                'COLLECT_LTO_WRAPPER=/usr/lib/gcc/x86_64-linux-gnu/4.8/lto-wrapper',
                'Target: x86_64-linux-gnu',
                "Configured with: ../src/configure -v --with-pkgversion='Ubuntu 4.8.2-19ubuntu1' --with-bugurl=file:///usr/share/doc/gcc-4.8/README.Bugs --enable-languages=c,c++,java,go,d,fortran,objc,obj-c++ --prefix=/usr --program-suffix=-4.8 --enable-shared --enable-linker-build-id --libexecdir=/usr/lib --without-included-gettext --enable-threads=posix --with-gxx-include-dir=/usr/include/c++/4.8 --libdir=/usr/lib --enable-nls --with-sysroot=/ --enable-clocale=gnu --enable-libstdcxx-debug --enable-libstdcxx-time=yes --enable-gnu-unique-object --disable-libmudflap --enable-plugin --with-system-zlib --disable-browser-plugin --enable-java-awt=gtk --enable-gtk-cairo --with-java-home=/usr/lib/jvm/java-1.5.0-gcj-4.8-amd64/jre --enable-java-home --with-jvm-root-dir=/usr/lib/jvm/java-1.5.0-gcj-4.8-amd64 --with-jvm-jar-dir=/usr/lib/jvm-exports/java-1.5.0-gcj-4.8-amd64 --with-arch-directory=amd64 --with-ecj-jar=/usr/share/java/eclipse-ecj.jar --enable-objc-gc --enable-multiarch --disable-werror --with-arch-32=i686 --with-abi=m64 --with-multilib-list=m32,m64,mx32 --with-tune=generic --enable-checking=release --build=x86_64-linux-gnu --host=x86_64-linux-gnu --target=x86_64-linux-gnu",
                'Thread model: posix',
                'gcc version 4.8.2 (Ubuntu 4.8.2-19ubuntu1)',
                ):
                self.writeln(l)

    def help(self):
        for l in (
            'Usage: gcc [options] file...'
            'Options:',
            '  -pass-exit-codes         Exit with highest error code from a phase',
            '  --help                   Display this information',
            '  --target-help            Display target specific command line options',
            '  --help={target|optimizers|warnings|params|[^]{joined|separate|undocumented}}[,...]',
            '                           Display specific types of command line options',
            '  (Use \'-v --help\' to display command line options of sub-processes)',
            '  --version                Display compiler version information',
            '  -dumpspecs               Display all of the built in spec strings',
            '  -dumpversion             Display the version of the compiler',
            '  -dumpmachine             Display the compiler\'s target processor',
            '  -print-search-dirs       Display the directories in the compiler\'s search path',
            '  -print-libgcc-file-name  Display the name of the compiler\'s companion library',
            '  -print-file-name=<lib>   Display the full path to library <lib>',
            '  -print-prog-name=<prog>  Display the full path to compiler component <prog>',
            '  -print-multi-directory   Display the root directory for versions of libgcc',
            '  -print-multi-lib         Display the mapping between command line options and',
            '                           multiple library search directories',
            '  -print-multi-os-directory Display the relative path to OS libraries',
            '  -print-sysroot           Display the target libraries directory',
            '  -print-sysroot-headers-suffix Display the sysroot suffix used to find headers',
            '  -Wa,<options>            Pass comma-separated <options> on to the assembler',
            '  -Wp,<options>            Pass comma-separated <options> on to the preprocessor',
            '  -Wl,<options>            Pass comma-separated <options> on to the linker',
            '  -Xassembler <arg>        Pass <arg> on to the assembler',
            '  -Xpreprocessor <arg>     Pass <arg> on to the preprocessor',
            '  -Xlinker <arg>           Pass <arg> on to the linker',
            '  -combine                 Pass multiple source files to compiler at once',
            '  -save-temps              Do not delete intermediate files',
            '  -pipe                    Use pipes rather than intermediate files',
            '  -time                    Time the execution of each subprocess',
            '  -specs=<file>            Override built-in specs with the contents of <file>',
            '  -std=<standard>          Assume that the input sources are for <standard>',
            '  --sysroot=<directory>    Use <directory> as the root directory for headers',
            '                           and libraries',
            '  -B <directory>           Add <directory> to the compiler\'s search paths',
            '  -b <machine>             Run gcc for target <machine>, if installed',
            '  -V <version>             Run gcc version number <version>, if installed',
            '  -v                       Display the programs invoked by the compiler',
            '  -###                     Like -v but options quoted and commands not executed',
            '  -E                       Preprocess only; do not compile, assemble or link',
            '  -S                       Compile only; do not assemble or link',
            '  -c                       Compile and assemble, but do not link',
            '  -o <file>                Place the output into <file>',
            '  -x <language>            Specify the language of the following input files',
            '                           Permissible languages include: c c++ assembler none',
            '                           \'none\' means revert to the default behavior of',
            '                           guessing the language based on the file\'s extension',
            '',
            'Options starting with -g, -f, -m, -O, -W, or --param are automatically',
            ' passed on to the various sub-processes invoked by gcc.  In order to pass',
            ' other options on to these processes the -W<letter> options must be used.',
            '',
            'For bug reporting instructions, please see:',
            '<file:///usr/share/doc/gcc-4.8/README.Bugs>.'
            ):
            self.writeln(l)

commands['/usr/bin/gcc'] = command_gcc
