#!/usr/bin/python3.5
# -*- coding: UTF-8 -*-

from helpers import files, transform
from helpers import settings

def clean(key):
    files.clearDirectory(key)

def unzip(key, url):
    files.unzip7z(url, key) #unzip main file

def generateSql(key, urlfile):
    lst = transform.getListHelpContext(key, urlfile)
    transform.getSQL(lst, key)

def run():
        # key = 'EXP'
        # url = '/home/joseechavez/Downloads/alas/prueba/{0}/{0}.chm'.format(key)
        # urlfile = '/home/joseechavez/Downloads/alas/prueba/{0}/{0}.txt'.format(key)

        # clean(key)
        # unzip(key, url)
        # generateSql(key, urlfile)

    for key in settings.OPTS:
        url = '/home/joseechavez/Downloads/alas/prueba/{0}/{0}.chm'.format(key)
        urlfile = '/home/joseechavez/Downloads/alas/prueba/{0}/{0}.txt'.format(key)

        clean(key)
        unzip(key, url)
        generateSql(key, urlfile)





