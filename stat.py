#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from odf.opendocument import load
from odf import text

import sys
reload(sys)
sys.setdefaultencoding('utf8')

TS = 0.0
XS = 0.0#xxdebug
DEBUG = 1

#cfg.py - https://docs.google.com/a/masols.com/document/d/1ge9HjJJ6Rfb-QjLZrZM5pOwWoWjZ5Wf-MgH0jqtMHwU/edit
from cfg import REVIEW
from cfg import UDATA

TITLE = "2014年 06 月 研发中心 绩效评估表"
REVIEW = REVIEW + "/2014-06"

def valuetype(val):
    valuetype="string"
    if isinstance(val,str): valuetype="string"
    if isinstance(val,int): valuetype="float"
    if isinstance(val,float): valuetype="float"
    if isinstance(val,bool): valuetype="boolean"
    return valuetype

def get_name(fn) :
    return fn.replace(".odt", "")

def get_num(para) :
    num = ""
    for child in para.childNodes :
        #pt=Para Text
        #<p>$text<p>
        if child.nodeType is child.TEXT_NODE :
            pt = child.data
            pt = pt.encode("utf8")
            print "[get_num] pt="+pt
            print "[get_num] type(pt)="+str(type(pt))
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
                    print "[get_num] pst="+pst
                    print "[get_num] type(pst)="+str(type(pst))
                    pst = filter(str.isdigit, pst)
                    if pst != "" : 
                        num += pst
    print "[get_num] num='"+num+"'"
    if num == "" :
        return "0"
    else :
        return num

def get_total_money() :
    global XS
    global UDATA
    for n,d in UDATA.items() :
        print "[get_total_money] name : '"+n+"'"
        print "[get_total_money] money : '"+str(d['qian'])+"'"
        XS += d['qian']

def cell(tr, val) :
    print "[cell] type="+str(type(val))
    tc = TableCell(valuetype=valuetype(val), value=str(val))
    tr.addElement(tc)
    p = P(stylename=tablecontents,text=str(val))
    tc.addElement(p)

def single_odt(path, uname, create) :
    global TS
    global XS
    global DEBUG
    global REVIEW
    global UDATA

    is_3m = UDATA[uname]['3m']
    money = UDATA[uname]['qian']

    print "[single_odt] path="+path
    doc = load(path)
    
    if create == 1 :
        # new row
        tr = TableRow()
        table.addElement(tr)
        # name column
        cell(tr, uname)
    
    contrib = []

    idx = 0
    for para in doc.getElementsByType(text.P):
        
        if idx >= 8 :
            break
        
        # no child
        if not para.hasChildNodes() :
            continue
        
        num = get_num(para)
        print "[single_odt] num='"+num+"'"
        
        if create == 1 :
            #table
            if idx == 6 :
                cell(tr, int(num)*is_3m)
            else :
                cell(tr, int(num))
        
        # store contrib
        contrib.append(int(num))
        
        idx += 1
    
    # every single contrib
    self_ticket = contrib[0]
    other_ticket = contrib[1]
    wiki = contrib[2]
    wiki_code = contrib[3]
    daima = contrib[4]
    bug = contrib[5]
    xuqiu = contrib[6]
    zuyuan = contrib[7]
    
    all_as_code = float(daima + xuqiu*10*is_3m + bug*20 + wiki_code/100 + wiki/20 + self_ticket/50 + other_ticket/40 + zuyuan/10)
    print "all_as_code="+str(all_as_code)
    
    if create == 0 :
        TS += all_as_code
    
    if create == 1 :
        print "money="+str(money)
        print "XS="+str(XS)
        print "TS="+str(TS)

        score = (all_as_code / TS) / (money / XS)

        cell(tr, all_as_code)               # all as score
        cell(tr, (all_as_code / TS))        # code score
        if DEBUG != 0 :
            cell(tr, money)                 # money
            cell(tr, (money / XS))          # money score
        cell(tr, score)
    
def all_odt(table, create) :
    for root, dirs, files in os.walk( REVIEW ):
        for fn in files:
            single_odt(root+"/"+fn, get_name(fn), create)

def header(table) :
    global DEBUG
    global TITLE

    # title

    tr = TableRow()
    table.addElement(tr)

    cell(tr, "")
    cell(tr, "")
    cell(tr, "")
    cell(tr, "")
    cell(tr, TITLE)

    # table header

    tr = TableRow()
    table.addElement(tr)
    
    cell(tr, "name")
    
    cell(tr, "self ticket")
    cell(tr, "other ticket")
    cell(tr, "wiki")
    cell(tr, "wiki code")
    cell(tr, "code")
    cell(tr, "bug ticket")
    cell(tr, "3m")
    cell(tr, "team member")
    
    cell(tr, "all as code")
    cell(tr, "code score")
    if DEBUG != 0 :
        cell(tr, "money")
        cell(tr, "money score")
    cell(tr, "score")

    cell(tr, "note")
    
def footer(table) :

    # footer row 1

    tr = TableRow()
    table.addElement(tr)
    
    cell(tr, "部门主管\n签字")
    cell(tr, "")
    cell(tr, "")
    cell(tr, "")
    
    cell(tr, "总经理")
    cell(tr, "")
    cell(tr, "")
    cell(tr, "")

    cell(tr, "不参加考核")
    cell(tr, "")
    cell(tr, "")
    cell(tr, "")
    
    # footer row 2

    tr = TableRow()
    table.addElement(tr)

    cell(tr, "人力资源\n审核")
    cell(tr, "")
    cell(tr, "")
    cell(tr, "")

    cell(tr, "签字")
    cell(tr, "")
    cell(tr, "")
    cell(tr, "")

    cell(tr, "人员备注")
    cell(tr, "")
    cell(tr, "")
    cell(tr, "")

# main

from odf.opendocument import OpenDocumentSpreadsheet
from odf.style import Style, TextProperties, ParagraphProperties
from odf.style import TableColumnProperties
from odf.text import P
from odf.table import Table, TableColumn, TableRow, TableCell

doc = OpenDocumentSpreadsheet()
# Create a style for the table content. One we can modify
# later in the word processor.
tablecontents = Style(name="Table Contents", family="paragraph")
tablecontents.addElement(ParagraphProperties(numberlines="false", linenumber="0"))
doc.styles.addElement(tablecontents)

# Create automatic styles for the column widths.
# We want two different widths, one in inches, the other one in metric.
# ODF Standard section 15.9.1
widthshort = Style(name="Wshort", family="table-column")
widthshort.addElement(TableColumnProperties(columnwidth="1.7cm"))
doc.automaticstyles.addElement(widthshort)

widthwide = Style(name="Wwide", family="table-column")
widthwide.addElement(TableColumnProperties(columnwidth="1.5in"))
doc.automaticstyles.addElement(widthwide)

# Start the table, and describe the columns
table = Table(name="jixiao")
table.addElement(TableColumn(numbercolumnsrepeated=4,stylename=widthshort))
table.addElement(TableColumn(numbercolumnsrepeated=3,stylename=widthwide))

# glue start
get_total_money()
header(table)
all_odt(table, 0)
all_odt(table, 1)
footer(table)
# glue end

doc.spreadsheet.addElement(table)
doc.save("jixiao", True)
