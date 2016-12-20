#!/usr/bin/python3.5
# -*- coding: UTF-8 -*-

import sys, pprint
from termcolor import colored
from subprocess import PIPE, run, call, Popen
import re

pp = pprint.PrettyPrinter(indent=4)

D_TEMP = 'tmp/' # route to temporary files

"""
Read files content and return as string
URL: string
"""
def getContent(url):
    # print colored( url, 'red');
    try:
        with open(url) as f:
            return f.read()
    except EnvironmentError: # parent of IOError, OSError *and* WindowsError where available
        print(colored(url+' COULD  NOT BE READ', 'red'))

"""
unzip shits
FILE: url to file
TYPE: zip or 7z
"""
def unzip(f, dest=''):
    command = 'unzip {0} -d {1}'.format(f, D_TEMP+dest);
    print(colored(command, 'blue'));
    p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE)
    return D_TEMP+dest

def clearDirectory(url):
    command = 'rm -Rf {0}'.format(D_TEMP+url);
    print(colored(command, 'blue'));
    p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE)

def findFile(folder, pattern):
    command = 'find {0} -type f -name {1}'.format(D_TEMP+folder, pattern);
    print(colored(command, 'blue'));
    p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE)
    return p.stdout.readline().decode('utf-8').strip()

# Print iterations progress
def printProgress (iteration, total, prefix = '', suffix = '', decimals = 2, barLength = 100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : number of decimals in percent complete (Int)
        barLength   - Optional  : character length of bar (Int)
    """
    filledLength    = int(round(barLength * iteration / float(total)))
    percents        = round(100.00 * (iteration / float(total)), decimals)
    bar             = '█' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),
    sys.stdout.flush()
    if iteration == total:
        sys.stdout.write('\n')
        sys.stdout.flush()
