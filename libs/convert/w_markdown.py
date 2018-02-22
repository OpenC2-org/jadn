"""
Translate JADN to Markdown property tables
"""

from __future__ import unicode_literals
from ..codec.jadn_defs import *
from ..codec.codec_utils import opts_s2d
from datetime import datetime


def markdown_dumps(jadn):
    """
    Produce property tables in Markdown format from JADN structure
    """

    hdrs = jadn["meta"]
    hdr_list = ["module", "title", "version", "description", "namespace"]
    mdown = '<!--\n'
    for h in list(set(hdrs) - set(hdr_list)):
        mdown += h + ': ' + str(hdrs[h]) + '\n'
    mdown += '-->\n\n'
    if 'title' in hdrs:
        mdown += '# ' + hdrs['title'] + '\n'
    if 'module' in hdrs:
        mdown += '## ' + hdrs['module']
        if 'version' in hdrs:
            mdown += ', version ' + hdrs['version']
        mdown += '\n'
    if 'description' in hdrs:
        mdown += hdrs['description'] + '\n'
    if 'namespace' in hdrs:
        mdown += '\nNamespace: ' + hdrs['namespace'] + '\n'

    mdown += '## 3.2 Primitive Types\n'
    mdown += '|Name|Type|Description|\n'
    mdown += '|---|---|---|\n'
    for td in jadn["types"]:                    # 0:type name, 1:base type, 2:type opts, 3:type desc, 4:fields
        if td[TTYPE] in PRIMITIVE_TYPES:
            mdown += '|' + td[TNAME] + '|' + td[TTYPE] + '|' + td[TDESC] + '|\n'
    mdown += '## 3.3 Vocabularies\n'
    n = 1
    for td in jadn['types']:
        if td[TTYPE] == 'Enumerated':
            mdown += '### 3.3.' + str(n) + ' ' + td[TNAME] + '\n'
            mdown += td[TDESC] + '\n\n'
            mdown += '|ID|Name|Description\n'
            mdown += '|---|---|---|\n'
            for fd in td[FIELDS]:
                mdown += '|' + str(fd[FTAG]) + '|' + fd[FNAME] + '|' + fd[EDESC] + '|\n'
            n += 1
    n = 1
    mdown += '## 3.4 Structure Types\n'
    for td in jadn['types']:
        if td[TTYPE] in {k for k in STRUCTURE_TYPES} - {'ArrayOf', 'Choice', 'Enumerated'}:
            mdown += '### 3.4.' + str(n) + ' ' + td[TNAME] + '\n'
            mdown += td[TDESC] + '\n\n'
            mdown += '| |' + td[TTYPE] + '| | | |\n'
            mdown += '|---|---|---|---:|---|\n'
            mdown += '|**ID**|**Name**|**Type**|**#**|**Description**|\n'
            for fd in td[FIELDS]:
                mdown += '|' + str(fd[FTAG]) + '|' + fd[FNAME] + '|' + fd[FTYPE]
                mdown += '|' + ('0..1' if opts_s2d(fd[FOPTS])['optional'] else '1')
                mdown += '|' + fd[FDESC] + '|\n'
            n += 1
        elif td[TTYPE] == 'Choice':
            n += 1
        elif td[TTYPE] == 'ArraryOf':
            n += 1

    return mdown


def markdown_dump(jadn, fname, source=""):
    with open(fname, "w") as f:
        if source:
            f.write('<!-- Generated from ' + source + ', ' + datetime.ctime(datetime.now()) + '-->\n')
        f.write(markdown_dumps(jadn))