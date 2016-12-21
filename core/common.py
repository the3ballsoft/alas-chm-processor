#!/usr/bin/python3.5
# -*- coding: UTF-8 -*-

from helpers import files, transform
from helpers import settings

# files been send wiht complete url
key = settings.OPTS[1]
url = '/home/joseechavez/Downloads/alas/prueba/{0}/{0}.chm'.format(key)
urlfile = '/home/joseechavez/Downloads/alas/prueba/{0}/{0}.txt'.format(key)


def clean():
    files.clearDirectory(key)

def unzip():
    files.unzip7z(url, key) #unzip main file

def generateSql():
    lst = transform.getListHelpContext(key, urlfile)
    transform.getSQL(lst, key)

def run():
    clean()
    unzip()
    generateSql()



