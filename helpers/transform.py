#!/usr/bin/python3.5
# -*- coding: UTF-8 -*-

from bs4 import BeautifulSoup

"""
extract raw text
"""
def extract_raw(content):
    soup = BeautifulSoup(content,  'html.parser')
    [s.extract() for s in soup('script')] # avoid scripts tags
    # get text
    text = soup.body.get_text()
    return text
"""
convert to predefined struct obj
map_ref: help context => number,
file_ref: topic id => file url or slug name,
content: full content of file,
raw: just text to search
"""
def transform(text, struct, folder, n):
    tmp = text.split('=')
    # print tmp
    obj = { "map_ref":  g_parse( tmp[0] ) ,
            "file_ref": g_parse( tmp[1] ) }
    ctn = getContent( folder, obj["file_ref"] ).decode('latin1')
    ctn = ctn.replace("'", "\\'").replace('"', '\\"')
    obj["content"] = ctn
    obj["raw"] = clean_text( obj["content"] ).replace("'", "\\'").replace('"', '\\"')

    # print colored('Proccesed: '+str(n)+' -> '+obj["file_ref"], 'blue')

    return obj
