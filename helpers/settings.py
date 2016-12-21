#!/usr/bin/python3.5
# -*- coding: UTF-8 -*-

import pprint

D_TEMP = 'tmp/'
PP = pprint.PrettyPrinter(indent=4)
OPTS = ['EXP', 'LEG', 'NOTES', 'REG']

sqlHeader = """
        -- -- Estructura de tabla para la tabla `alas_leg` --
        CREATE TABLE IF NOT EXISTS `help_text` (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `help_type` varchar(255) NOT NULL,
        `map_ref` varchar(255) NULL,
        `file_ref` varchar(255) NOT NULL,
        `text_content` longtext,
        `html_content` longtext NOT NULL,
        PRIMARY KEY (`id`)
        ) ENGINE=InnoDB  DEFAULT CHARSET=utf8;
        --
        -- Volcado de datos para la tabla `help_text`
        --
        """
