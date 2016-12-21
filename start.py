#!/usr/bin/python3.5
# -*- coding: UTF-8 -*-

import sys
from termcolor import colored
from core.common import run, clean, unzip, generateSql

"""
Execute individual taks by command
"""
if len(sys.argv) > 1 and sys.argv[1] in locals():
    print( colored('running {0}'.format(sys.argv[1]), 'green') )
    func = locals()[sys.argv[1]]
    func()
    sys.exit()

print( colored('Default running...', 'green') )
run()
