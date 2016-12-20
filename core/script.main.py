#!/usr/bin/python
# -*- coding: latin1 -*-

import sys, pprint
from bs4 import BeautifulSoup
from termcolor import colored
import re

pp = pprint.PrettyPrinter(indent=4)



# PARAMS .hhp .hhc /folder-htmlfiles
# print 'Argument List:', str(sys.argv)
# if(len(sys.argv) < 3):
    # print 'arguments(3): .hhp  /folder-htmlfiles .hhc'
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
    ctn = getContent( folder, obj["file_ref"] ).decode('latin1')
    ctn = ctn.replace("'", "\\'").replace('"', '\\"')
    obj["content"] = ctn
    obj["raw"] = clean_text( obj["content"] ).replace("'", "\\'").replace('"', '\\"')

    print colored('Proccesed: '+str(n)+' -> '+obj["file_ref"], 'blue')

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
    # filehhc = sys.argv[3]

    strOut = """
            -- -- Estructura de tabla para la tabla `alas_leg` --
            CREATE TABLE IF NOT EXISTS `alas_leg` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `map_ref` varchar(255) NOT NULL,
            `file_ref` varchar(255) NOT NULL,
            `content` longtext NOT NULL,
            `raw` longtext,
            PRIMARY KEY (`id`)
            ) ENGINE=InnoDB  DEFAULT CHARSET=latin1;
            --
            -- Volcado de datos para la tabla `help_context`
            --
            INSERT INTO `alas_leg` (`id`, `map_ref`, `file_ref`, `content`, `raw`) VALUES
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

    nfile = 'out.sql'
    rec = 1
    l = len(struct)-1
    f = open(nfile,'wb')
    f.write(strOut) # write header content
    for ind, obj in enumerate(struct):
        row = '(null, "'+obj["map_ref"]+'", "'+obj["file_ref"]+'", "'+obj["content"]+'", "'+obj["raw"]+'"),'
        if ind == l:
            row = row[:-1]+';'  # terminate excution
            f.write(row.encode('utf8')) # write normal line
        # SPLIT FILES 1000 regs
        # elif ind > 1000*rec:
            # f.write((row[:-1]+';').encode('utf8')) # write last line of file
            # f.close()
            # f = open(str(rec)+nfile,'wb')
            # f.write(strOut) # write header content for new file
            # rec += 1
        # SPLIT FILES 1000 regs END
        else:
            f.write(row.encode('utf8')) # write normal line


        printProgress(ind, l, prefix = 'Progress:', suffix = 'Complete', barLength = 50)


    f.close() # you can omit in most cases as the destructor will call it
    print colored('\nSaved: out.sql', 'green')

    # pp.pprint(struct)

main()

