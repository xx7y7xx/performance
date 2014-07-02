#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from odf.opendocument import load
from odf import text

import sys
reload(sys)
sys.setdefaultencoding('utf8')

def valuetype(val):
    valuetype="string"
    if isinstance(val,str): valuetype="string"
    if isinstance(val,int): valuetype="float"
    if isinstance(val,float): valuetype="float"
    if isinstance(val,bool): valuetype="boolean"
    return valuetype

def cell(tr, val, style = None) :
    print "[cell] type="+str(type(val))
    if style is None :
        tc = TableCell(valuetype=valuetype(val), value=str(val))
        tr.addElement(tc)
        p = P(stylename=tablecontents,text=str(val))
    else :
        tc = TableCell(stylename=style, valuetype=valuetype(val), value=str(val))
        tr.addElement(tc)
        p = P(stylename=style,text=str(val))

    tc.addElement(p)

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

# chenyang20140702-start
# create style for big title
bigtitle = Style(name="Large number", family="table-cell")
bigtitle.addElement(TextProperties(fontfamily="WenQuanYi Micro Hei", fontsize="20pt", fontsizeasian="50pt"))
bigtitle.addElement(TableColumnProperties(columnwidth="17cm"))
doc.styles.addElement(bigtitle)
# chenyang20140702-end

# Start the table, and describe the columns
table = Table(name="big_title")
#table.addElement(TableColumn(numbercolumnsrepeated=4,stylename=widthshort))
#table.addElement(TableColumn(numbercolumnsrepeated=3,stylename=widthwide))

# glue start
tr = TableRow()
table.addElement(tr)
cell(tr, "a部b门主c管", bigtitle)
# glue end

doc.spreadsheet.addElement(table)
doc.save("big_title", True)
