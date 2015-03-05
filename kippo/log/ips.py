#!/usr/bin/env python
import os
import sys
from subprocess import Popen, PIPE

for f in os.listdir('.'):
    try:
        new = True
        f = open(f, 'r')
        for line in f:
            if 'HoneyPotTransport,' in line:
                try:
                    ip = line.split('HoneyPotTransport,')[1].split(',')[1].split('] ')[0]
                    sys.stdout.write(ip)
                    who = Popen(['whois', ip], stdout=PIPE, stderr=PIPE)
                    for l in who.communicate()[0].split('\n'):
                        if 'netname:' in l:
                            sys.stdout.write('\t%s' % l.split(' ')[-1])
                        elif 'country:' in l and new:
                            new = False
                            sys.stdout.write('\t%s' % l.split(' ')[-1])
                    sys.stdout.write('\n')
                    new = True
                except:pass
    except: pass
