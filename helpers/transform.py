#!/usr/bin/python3.5
# -*- coding: UTF-8 -*-

from bs4 import BeautifulSoup as Soup
from termcolor import colored
from .settings import D_TEMP, PP, sqlHeader
from .files import getContent, getContentHtm, scanFolder, printProgress, createPath
import unicodedata

def cleanContent(ctn):
    # ctn = unicodedata.normalize('NFD', ctn).encode('ascii', 'ignore').decode('ascii')
    return ctn.replace("'", "\\'").replace('"', '\\"')

"""
remove accent mark, uppercas
and special characters
"""
def slug(value):
    value = unicodedata.normalize('NFD', value).encode('ascii', 'ignore').decode('ascii')
    value = value.strip().lower()
    return value

"""
extract raw text
"""
def extract_raw(content):
    if not content: return ''
    soup = Soup(content,  'html.parser')
    [s.extract() for s in soup('script')] # avoid scripts tags
    # get text
    if soup.body:
        text = soup.body.get_text()
    else:
        return content
    return text.replace('"', '')

"""
try to get content
with no exact name of file
"""
def extractContent(name, path, ffolder=None):
    if ffolder:
        for f in ffolder:
            # print(slug(f), ' = ', colored(name, 'green'))
            if slug(f) == name:
                ffolder.remove(f)    # delete found item
                # print(colored(f, 'green'));
                return getContentHtm(path+'/'+f)
        print('Not found in directory: ', colored(name, 'red'));
        return 'ERROR'
    else:
        # print('without list: ', colored(name, 'red'));
        return getContentHtm(path+'/'+name)

"""
extract list of htm files with context help form
file hmxp and return array of objects with its information
"""
def getListHelpContext(key, url):
    out = []
    notfound = 0
    content = getContentHtm(url) # get content and avoid spaces
    lst = content.splitlines();
    ffolder = scanFolder(D_TEMP+key, False) # get list of htm files
    print('Folder: '+str(len(ffolder)), 'List: '+str(len(lst)))
    for l in lst:
        tmp = l.split('=')
        obj = { 'file_ref': slug( tmp[0]).replace('.', '_')+'.htm',
                'help_type': key.upper(),
                'map_ref': tmp[1] }
        # send ffolder to remove whom found
        ctn = extractContent( obj['file_ref'], D_TEMP+key, ffolder )
        if ctn == 'ERROR': notfound+=1
        obj["html_content"] = cleanContent(ctn)
        obj["text_content"] = extract_raw( obj["html_content"] )
        out.append(obj)

    # print('Folder: '+str(len(ffolder)), 'From list: '+str(len(out)))
    # save files without help context
    for l in ffolder:
        obj = { 'file_ref': slug(l),
                'help_type': key.upper(),
                'map_ref': '' }
        ctn = extractContent( l, D_TEMP+key )
        if ctn == 'ERROR': notfound+=1
        obj["html_content"] = cleanContent(ctn)
        obj['text_content'] = extract_raw( obj["html_content"] )
        out.append(obj)

    print(colored('Total: ', 'green')+str(len(out)))
    print(colored('Not Found: '+str(notfound), 'red'))
    return out

def getSQL(struct, key):
    s_path = D_TEMP+key+'/output/'
    createPath(s_path); # create path if dont exist
    # PP.pprint(lst)

    nfile = '%s.sql' % key
    l = len(struct)-1
    f = open(s_path+nfile,'wb')
    f.write(sqlHeader.encode('utf8')) # write header content
    for ind, obj in enumerate(struct):
        row = """
        INSERT INTO `help_text`
        (`id`, `help_type`, `map_ref`, `file_ref`, `text_content`, `html_content`)
        VALUES
        (null, "%s", "%s", "%s", "%s", "%s");
        """ % (obj['help_type'], obj['map_ref'], obj['file_ref'], obj['text_content'], obj['html_content'])

        f.write(row.encode('utf8')) # write normal line
        printProgress(ind+1, l, prefix = 'Progress:', suffix = 'Complete', barLength = 50)

    f.close() # you can omit in most cases as the destructor will call it
    print(colored('\nSaved: %s.sql' % key, 'green'))
