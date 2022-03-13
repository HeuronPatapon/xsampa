"""
    Panflute filter to type phonetics with X-SAMPA and rendering it in IPA. 

    X-SAMPA is an ascii-friendly format, making typing easier. 


    Syntax
    -----
    basic syntax
    :   `[tEst]{.xsampa}`{.md}
        becomes
        tɛst

    bracket management
    :   [tEst]{.xsampa note=phone}
        becomes
        [tɛst]

    :   [tEst]{.xsampa note=phonm}
        becomes
        /tɛst/

    :   [tEst]{.xsampa note=graphm}
        becomes
        ‹tɛst›
"""
from typing import *
import doctest
import unittest


import panflute as pf


from .converters import XSAMPA


def action(elem, doc):
    if isinstance(elem, pf.Span):
        if "xsampa" in elem.classes:
            elem.content: list[pf.Str] = [
                pf.Str(XSAMPA.to_ipa(pf.stringify(child)))
                for child in elem.content
            ]
        match elem.attributes.get("note"):
            case "phone":
                elem.content.insert(0, pf.Str("["))
                elem.content.append(pf.Str("]"))
            case "phonm":
                elem.content.insert(0, pf.Str("/"))
                elem.content.append(pf.Str("/"))
            case "graphm":
                elem.content.insert(0, pf.Str("‹"))
                elem.content.append(pf.Str("›"))

    return elem


def main(doc=None):
    return pf.run_filter(action, doc=doc)


if __name__ == '__main__':
    main()
