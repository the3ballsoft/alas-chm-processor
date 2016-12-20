#!/usr/bin/python3.5
# -*- coding: UTF-8 -*-

from bs4 import BeautifulSoup as Soup
from termcolor import colored
from .settings import D_TEMP, PP
from .files import getContent, scanFolder
import unicodedata, re

"""
remove accent mark, uppercas
and special characters
"""
def slug(value):
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub('[^\w\s-]', '', value).strip().lower()
    return value

"""
extract raw text
"""
def extract_raw(content):
    soup = Soup(content,  'html.parser')
    [s.extract() for s in soup('script')] # avoid scripts tags
    # get text
    text = soup.body.get_text()
    return text

"""
try to get content
with no exact name of file
"""
def extractContent(name, ffolder, path):
    def aprox(text):
        text = text.replace('б', 'i')
        return text

    # first try
    # print(len(ffolder))
    for f in ffolder:
        # print(f, name)
        if f == name:
            # print(colored(f, 'red'))
            ffolder.remove(f) # delete found item
            return getContent(path+'/'+f)
    # seccond
    # print(len(ffolder))
    for f in ffolder:
        # print(aprox(f), name)
        if aprox(f) == name:
            # print(colored(aprox(f), 'red'))
            ffolder.remove(f) # delete found item
            return getContent(path+'/'+f)
    print(colored(f, 'red')+' == '+colored(name, 'green'))

"""
convert to predefined struct obj
map_ref: help context => number,
file_ref: topic id => file url or slug name,
content: full content of file,
raw: just text to search
"""
def toObject(l, ffolder, path):
    obj = { 'file_ref': slug( l.get('href') )+".htm",
            'map_ref': l.get('value') }
    obj["content"] = extractContent( obj['file_ref'], ffolder, path )
    # obj["raw"] = extract_raw( obj["content"] )
    return obj

"""
extract list of htm files with context help form
file hmxp and return array of objects with its information
"""
def getList(key):
    out = []
    url = D_TEMP+key+'/project.hmxp'
    content = getContent(url)
    soup = Soup(content, 'html.parser')
    numbers = soup.find('helpcontext-numbers').findAll('helpcontext-number')
    print( colored("Found in .hmxp file with help context ",
        'blue')+colored(str(len(numbers)), 'green')  ) #DEBUG

    ffolder = scanFolder( D_TEMP+key, False )
    for n in numbers:
        out.append( toObject(n, ffolder, D_TEMP+key) )

    PP.pprint(ffolder)
    # PP.pprint(out)
    return out

def getSQL():
    pass
