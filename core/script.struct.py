#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, pprint
from bs4 import BeautifulSoup
from termcolor import colored

pp = pprint.PrettyPrinter(indent=4)

def main():
    struct = []
    filehhc = sys.argv[1]

    # strOut = """
            # -- -- Estructura de tabla para la tabla `alas_leg` --
            # CREATE TABLE IF NOT EXISTS `alas_leg` (
            # `id` int(11) NOT NULL AUTO_INCREMENT,
            # `map_ref` varchar(255) NOT NULL,
            # `file_ref` varchar(255) NOT NULL,
            # `content` longtext NOT NULL,
            # `raw` longtext,
            # PRIMARY KEY (`id`)
            # ) ENGINE=InnoDB  DEFAULT CHARSET=utf-8;
            # --
            # -- Volcado de datos para la tabla `help_context`
            # --
            # INSERT INTO `alas_leg` (`id`, `map_ref`, `file_ref`, `content`, `raw`) VALUES
            # """

    def build(child):
        if child.name == 'object':
            tmp = {}
            for pa in enumerate(child.findChildren()):
                if pa[1].attrs['name'] == 'Name':
                    tmp['name'] = pa[1].attrs['value'].encode('utf-8')
                if pa[1].attrs['name'] == 'Local':
                    tmp['file_url'] = pa[1].attrs['value'].encode('utf-8')
            return tmp
        elif child.name == 'ul':
            tmp = []
            for ch in child.children:
                if ch.name:
                    tmp.append( build( ch ) )
            return tmp


    # # READ FILE .hhp
    with open(filehhc, 'r') as f:
        html = f.read().replace("<LI>", "")
        soup = BeautifulSoup(html, 'html.parser')
        for child in soup.find('ul').children:
            if child.name:
                struct.append( build(child) )

    pp.pprint(struct)

main()
