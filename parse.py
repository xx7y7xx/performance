#!/usr/bin/env python
# -*- coding: utf-8 -*-

#/**************************************************************************
# *
# *  This file is part of the OSC(Open Source Communit).
# *  Copyright (C) by SanPolo Co.Ltd.
# *  All rights reserved.
# *
# *  See http://osc.spolo.org/ for more information.
# *
# *  SanPolo Co.Ltd
# *  http://www.spolo.org/  spolo@spolo.org sales@spolo.org
# *
#**************************************************************************/

# common lib
import os
import re

# need opendocument lib
from odf import text
from odf.opendocument import load
from odf.opendocument import OpenDocumentSpreadsheet
from odf.style import Style, TextProperties, ParagraphProperties
from odf.style import TableColumnProperties
from odf.style import TableRowProperties
from odf.text import P
from odf.table import Table, TableColumn, TableRow, TableCell

# need download file from web.
import urllib2
from urllib2 import HTTPError

# fix chinese in code
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def _get_num(para) :
    num = ""
    for child in para.childNodes :
        #pt=Para Text
        #<p>$text<p>
        if child.nodeType is child.TEXT_NODE :
            pt = child.data
            pt = pt.encode("utf8")
            #print "[get_num] pt="+pt
            #print "[get_num] type(pt)="+str(type(pt))
            pt = filter(str.isdigit, pt)
            if pt != "" :
                num += pt
        #pst=Para Span Text
        #<p>
        #  <span>$text</span>
        #  <span>$text</span>
        #</p>
        if child.nodeType is child.ELEMENT_NODE :
            for chd in child.childNodes :
                if chd.nodeType is chd.TEXT_NODE :
                    pst = chd.data
                    pst = pst.encode("utf8")
                    #print "[get_num] pst="+pst
                    #print "[get_num] type(pst)="+str(type(pst))
                    pst = filter(str.isdigit, pst)
                    if pst != "" :
                        num += pst
    #print "[get_num] num='"+num+"'"
    if num == "" :
        return "0"
    else :
        return num

def parse_odt(path) :

    doc = load(path)
    
    contrib = []

    idx = 0
    for para in doc.getElementsByType(text.P):
        
        if idx >= 8 :
            break
        
        # no child
        if not para.hasChildNodes() :
            continue
        
        num = _get_num(para)
        
        # store contrib
        contrib.append(int(num))
        
        idx += 1
    
    return contrib

def create_ods(filename):
    doc = OpenDocumentSpreadsheet()
    #doc.spreadsheet.addElement(table)
    #doc.save(filename, True) # add "ods" as suffix
    doc.save(filename) # not add "ods" as suffix

#EOF
