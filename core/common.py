#!/usr/bin/python3.5
# -*- coding: UTF-8 -*-

from helpers import files, transform

# files been send wiht complete url
url = '/home/joseechavez/Downloads/alas/prueba/alasnota.ZIP'
key = 'notas'


def clean():
    files.clearDirectory(key)

def unzip():
    files.unzip(url, key) #unzip main file
    hmxz = files.findFile(key, '*.hmxz') #find file hmxz
    files.unzip(hmxz, key) #unzip hmxz file

def getList():
    transform.getList(key)

def run():
    clean()
    unzip()
    getList()



