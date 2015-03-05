#!/usr/bin/env python

import os
for f in os.listdir('.'):
    try:
        f = open(f, 'r')
        for line in f:
            if 'login attempt [' in line:
                print line.split('login attempt [')[1].split('] failed')[0]
    except: pass
