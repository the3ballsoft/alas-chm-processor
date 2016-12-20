#!/usr/bin/python
# -*- coding: latin1 -*-

# Genera sql con legislacion y notas
# de los archivos html que no tenian help_context
# legislacion total: 5931, con help_context: 5440, results = 491
# notas total: 146, con help_context: 139, results = 7


import sys, pprint
from bs4 import BeautifulSoup
from termcolor import colored
import re

pp = pprint.PrettyPrinter(indent=4)



# PARAMS .hhp .hhc /folder-htmlfiles
# print 'Argument List:', str(sys.argv)
# if(len(sys.argv) < 3):
    # print 'arguments(3): .hhp  /folder-htmlfiles
    # exit()



# HELPER FUNCTION
def g_parse(txt):
    tmp = txt.lstrip().rstrip().decode('latin1')
    return tmp

def getContent(folder, fname):
    url = folder+fname
    # print colored( url, 'red');
    try:
        with open(url) as f:
            content = f.read()
            return content
    except EnvironmentError: # parent of IOError, OSError *and* WindowsError where available
        print colored(url+' COULD  NOT BE READ', 'red')

def clean_text(content):
    # print colored(content, 'green')
    soup = BeautifulSoup(content,  'html.parser')
    [s.extract() for s in soup('script')] # avoid scripts tags
    # get text
    text = soup.body.get_text()
    return text

def parse(text, struct, folder, n):
    tmp = text.split('=')
    # print tmp
    obj = { "map_ref":  g_parse( tmp[0] ) ,
            "file_ref": g_parse( tmp[1] ) }

    print colored('Proccesed: '+str(n)+' -> '+obj["file_ref"], 'blue')

    struct.append(obj)

def extract(struct, folder, namefiel):
    obj = { "map_ref": 'NULL' ,
            "file_ref": g_parse( namefiel ) }

    ctn = getContent( folder, obj["file_ref"] ).decode('latin1')
    ctn = ctn.replace("'", "\\'").replace('"', '\\"')
    obj["html_content"] = ctn
    obj["text_content"] = clean_text( obj["html_content"] ).replace("'", "\\'").replace('"', '\\"')

    # obj["help_type"] = 'NOTE'
    obj["help_type"] = 'LEG'

    struct.append(obj)

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

def main():
    '''
    [{map_ref: 231234, file_ref: '', content: '', raw: ''}]
    '''
    struct = []
    filehhp = sys.argv[1]
    folder = sys.argv[2]

    strOut = """
            -- -- Estructura de tabla para la tabla `HelpText` --
            CREATE TABLE IF NOT EXISTS `HelpText` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `help_type` varchar(255) NOT NULL,
            `map_ref` varchar(255) NULL,
            `file_ref` varchar(255) NOT NULL,
            `text_content` longtext NOT NULL,
            `html_content` longtext NOT NULL,
            PRIMARY KEY (`id`)
            ) ENGINE=InnoDB  DEFAULT CHARSET=latin1;
            --
            -- Volcado de datos para la tabla `help_context`
            --
            INSERT INTO `HelpText` (`help_type`, `map_ref`, `file_ref`, `text_content`, `html_content`) VALUES
            """

    # READ FILE .hhp
    with open(filehhp, "r") as ins:
        sw = False
        n = 0
        for line in ins:
            if sw:
                n += 1
                parse(line, struct, folder, n);
            elif g_parse(line) == '[ALIAS]':
                sw = True

            # if n > 20: break



    print colored('Proccesed: '+str(len(struct)-1), 'green')

    # read files htm from folder
    import glob
    htms = glob.glob(folder+"*.htm")
    res = []

    for ind, htm in enumerate(htms):
        fil =  htm.split('/')[-1].decode('utf-8')
        sw = False
        for ind2, prev in enumerate(struct):
            # print("compara: "+fil+" and "+prev["file_ref"])
            # raw_input("")
            if (fil == prev["file_ref"]):
                sw = True
                break
        if (sw == False):
            extract(res, folder, fil)

    print len(res)





    nfile = 'out.sql'
    rec = 1
    l = len(res)-1
    f = open(nfile,'wb')
    f.write(strOut) # write header content
    for ind, obj in enumerate(res):
        row = '("'+obj["help_type"]+'", '+obj["map_ref"]+', "'+obj["file_ref"]+'", "'+obj["text_content"]+'", "'+obj["html_content"]+'"),'
        if ind == l:
            row = row[:-1]+';'  # terminate excution
            f.write(row.encode('utf8')) # write normal line
        else:
            f.write(row.encode('utf8')) # write normal line


        printProgress(ind, l, prefix = 'Progress:', suffix = 'Complete', barLength = 50)


    f.close() # you can omit in most cases as the destructor will call it
    print colored('\nSaved: out.sql', 'green')

    # pp.pprint(res)

main()

