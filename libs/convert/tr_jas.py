"""
Translate JADN to and from JAS (JADN Abstract Syntax)
"""

import re
from .jas_parse import jasParser
from ..codec.jadn_defs import *
from ..codec.codec import is_primitive
from ..codec.codec_utils import opts_s2d, opts_d2s
from copy import deepcopy
from datetime import datetime
from textwrap import fill


class Jastype:

    def __init__(self):
        types = [
            ("Binary", "BINARY"),           # OCTET STRING
            ("Boolean", "BOOLEAN"),         # BOOLEAN
            ("Integer", "INTEGER"),         # INTEGER
            ("Number", "REAL"),             # REAL
            ("String", "STRING"),           # UTF8String
            ("Array", "ARRAY_OF"),          # SEQUENCE OF
            ("Choice", "CHOICE"),           # CHOICE
            ("Enumerated", "ENUMERATED"),   # ENUMERATED
            ("Map", "MAP"),                 # SET
            ("Record", "RECORD")            # SEQUENCE
        ]
        self._ptype = {t[0]: t[1] for t in types}
        self._jtype = {t[1]: t[0] for t in types}

    def ptype(self, jt):            # Convert to source (JAS) type
        return self._ptype[jt] if jt in self._ptype else jt

    def jtype(self, pt):            # Convert to JADN type
        return self._jtype[pt] if pt in self._jtype else pt


def _parse_import(import_str):
    tag, ns, uid = re.match("(\d+),\s*(\w+),\s*(.+)$", import_str).groups()
    return [int(tag), ns, uid]


def _nstr(v):       # Return empty string if None
    return v if v else ""

def _topts(v):
    pt = Jastype()
    opts = {}
    for o in v if v else []:
        if isinstance(o, list) and o[0] == "PATTERN":
            opts.update({"pattern": "".join(o[1])})
        elif isinstance(o, str):              # TODO: do better checking that type=Array goes with topts=#aetype
            opts.update({"aetype": pt.jtype(o)})
        else:
            print("Unknown type option", o, v)
    return opts_d2s(opts)

def _fopts(v):      # TODO: process min/max/range option
    opts = {}
    for o in v if v else []:
        if isinstance(o, str) and o.lower() == "optional":
            opts.update({"optional": True})
        elif isinstance(o, list) and o[0] == ".&":
            opts.update({"atfield": o[1]})
        else:
            print("Unknown field option", o, v)
    return opts_d2s(opts)


def jas_loads(jas_str):
    """
    Load abstract syntax from JAS file
    """

    parser = jasParser(parseinfo=True, )

    ast = parser.parse(jas_str, 'jas', trace=False)
    meta = {}
    for m in ast["metas"]:
        k = m["key"]
        if k.lower() == "import":
            meta[k] = [[int(x), y.strip(), z.strip()] for x, y, z in (s.split(",") for s in m["val"])]
        else:
            meta[k] = " ".join(m["val"])

    pt = Jastype()
    types = []
    for t in ast["types"]:
        fields = []
        tdesc = t["td1"]
        topts = t["topts"]
        if t["f"]:
            tdesc = t["f"]["td2"] if t["f"]["td2"] else tdesc
            tf = t["f"]["fields"]
            for n in range(len(tf)-1):          # shift field descriptions up to corresponding fields
                tf[n]["fd2"] = tf[n+1]["fd1"]
            for n, f in enumerate(t["f"]["fields"]):
                fdesc = f["fd2"]
                tag = None
                if t["type"].lower() == "record":
                    tag = n + 1
                elif isinstance(f["tag"], str):
                    tag = int(f["tag"])
                else:
                    print("Error: missing tag", t["name"], f["name"])   # TODO: make all errors exceptions
                if tag is not None:
                    if t["type"].lower() == "enumerated":
                        fields.append([tag, f["name"], _nstr(fdesc)])
                    else:
                        fields.append([tag, f["name"], pt.jtype(f["type"]), _fopts(f["fopts"]), _nstr(fdesc)])
        tdef = [t["name"], pt.jtype(t["type"]), _topts(topts), _nstr(tdesc)]
        types.append(tdef if is_primitive(tdef[1]) else tdef + [fields] )
    jadn = {"meta": meta, "types": types}
    return jadn


def jas_load(fname):
    with open(fname) as f:
        return jas_loads(f.read())
