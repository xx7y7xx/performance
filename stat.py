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

# Make sure change to current dir of this script, and then run it.

import os
import time

#import argparse  # new in python2.7
import optparse   # old python

from odf.opendocument import load
from odf import text

from odf.opendocument import OpenDocumentSpreadsheet
from odf.style import Style, TextProperties, ParagraphProperties
from odf.style import TableColumnProperties
from odf.style import TableRowProperties
from odf.text import P
from odf.table import Table, TableColumn, TableRow, TableCell

import urllib2
from urllib2 import urlopen
import socket

import json

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from xxutils import getDate
from xxutils import get_name

def valuetype(val):
    valuetype="string"
    if isinstance(val,str): valuetype="string"
    if isinstance(val,int): valuetype="float"
    if isinstance(val,float): valuetype="float"
    if isinstance(val,bool): valuetype="boolean"
    return valuetype

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
        return 0
    else :
        return int(num)

def get_total_creat() :
    global XS
    global UDATA
    global DEBUG
    for n,d in UDATA.items() :
        if DEBUG is 1 : 
            print "[get_total_creat] name : '"+n+"'"
            print "[get_total_creat] creat : '"+str(d['creat'])+"'"
        XS += d['creat']

def get_3m_data():
  global M3DATA
  global MONTH
  url = "http://192.168.0.61:8080/sysop.api.query?xpath=%2Fjcr%3Aroot%2Fcontent%2Fusers%2F_chenyang_40masols.com%2Foa%2Fm3%2F%2A+order+by+%40month+descending&limit=30&offset=0"
  print("url: %s" % url)

  try:
    response = urlopen(url, timeout = 30)
  except urllib2.HTTPError as e:
    msg = "URL : %s\n" % url
    msg += 'Server return code : %s' % e.code
    print(msg)
    sys.exit(1)
  except urllib2.URLError as e:
    print(('Unexpected exception thrown:', e.args))
    sys.exit(2)
  except socket.timeout as e:
    print(('Server timeout:', e.args))
    sys.exit(3)

  raw_data = response.read().decode('utf-8')
  json_obj = json.loads(raw_data)
  rows = json_obj["rows"]
  for row in rows:
    # __node_name__ = 201507
    if row["__node_name__"] != MONTH:
      continue
    M3DATA = row["userlist"]

def get_udata():
  global UDATA

  UDATA = {}

  import random
  url = "http://www.xuanran001.com/usercenter/xingzheng/renyuanguanli.html?xpath=%2Fjcr%3Aroot%2Fcontent%2Fusers%2F*%20%5B%40role%3D%27%2Fcontent%2Fuserrole%2Fchengxuyuan%27%5D&rows=30&_=" + str(random.randint(1, 1000000))
  print("url: %s" % url)

  try:
    response = urlopen(url, timeout = 30)
  except urllib2.HTTPError as e:
    msg = "URL : %s\n" % url
    msg += 'Server return code : %s' % e.code
    print(msg)
    sys.exit(1)
  except urllib2.URLError as e:
    print(('Unexpected exception thrown:', e.args))
    sys.exit(2)
  except socket.timeout as e:
    print(('Server timeout:', e.args))
    sys.exit(3)

  raw_data = response.read().decode('utf-8')
  json_obj = json.loads(raw_data)
  rows = json_obj["rows"]
  for row in rows:
    name = row["userID"].split("@")[0]
    UDATA[name] = {}

    print("userID=%s" % name)

    if "jcr:creat" in row:
      UDATA[name]["creat"] = (int(row["jcr:creat"])-20140000000)/99
    else:
      UDATA[name]["creat"] = 0
      print("'jcr:creat' property is missing in this node")

    code_quality_map = {
      "webfe" : 0.5,
      "webbe" : 1,
      "gh3d"  : 1
    }

    if "oa_group" in row:
      UDATA[name]["quality"] = code_quality_map[row["oa_group"]]
    else:
      UDATA[name]["quality"] = code_quality_map["webfe"]
      print("'oa_group' property is missing in this node")

    print("[get_udata] %s : %i : %i" % ( name, UDATA[name]["creat"], UDATA[name]["quality"] ))

  print UDATA

def cell(tr, val, style = None) :
    print "[cell] type=%s" % str(type(val))
    print "[cell] type=%s" % str(val)
    if style is None :
        tc = TableCell(valuetype=valuetype(val), value=str(val))
    else :
        tc = TableCell(stylename=style, valuetype=valuetype(val), value=str(val))
    tr.addElement(tc)
    p = P(stylename=tablecontents,text=str(val))
    tc.addElement(p)

def single_odt(path, uname, create, table) :
    global TS
    global XS
    global DEBUG
    global REVIEW
    global UDATA
    global M3DATA

    print "[single_odt] stat " + uname

    is_3m = uname in M3DATA
    creat = UDATA[uname]['creat']
    quality = UDATA[uname]['quality']
    print "[single_odt] quality of " + uname + " is " + str(quality)

    print "[single_odt] path="+path
    doc = load(path)
    
    if create == 1 :
        # new row
        tr = TableRow()
        table.addElement(tr)
        # name column
        cell(tr, uname)
        cell(tr, quality)
    
    contrib = []

    idx = 0
    for para in doc.getElementsByType(text.P):
        
        if idx >= 8 :
            break
        
        # no child
        if not para.hasChildNodes() :
            continue
        
        num = get_num(para)
        print "[single_odt] idx='%s'" % str(idx)
        print "[single_odt] num='%s'" % str(num)

        if idx == 5:
            print "[single_odt] bug column"
            # bug number not large than 100
            #assert num < 100
            if num >= 100:
                print "[single_odt] bug number large than 100"
                num = 0.0
        
        if create == 1 :
            # is 3month
            if idx == 6 :
                cell(tr, num*is_3m)
            else :
                cell(tr, num)
        
        # store contrib
        contrib.append(num)
        
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
    
    all_as_code = float(daima*quality + xuqiu*10*is_3m*quality + bug*20 + wiki_code/100 + wiki/20 + self_ticket/50 + other_ticket/40 + zuyuan*TMQ)
    print "all_as_code = float(daima*quality + xuqiu*10*is_3m*quality + bug*20 + wiki_code/100 + wiki/20 + self_ticket/50 + other_ticket/40 + zuyuan*TMQ)"
    print str(daima)+"*"+str(quality)+"+"+str(xuqiu)+"*10*"+str(is_3m)+"*"+str(quality)+"+"+str(bug)+"*20"+"+"+str(wiki_code)+"/100"+"+"+str(wiki)+"/20"+"+"+str(self_ticket)+"/50"+"+"+str(other_ticket)+"/40"+"+"+str(zuyuan)+"*"+str(TMQ)
    print "all_as_code="+str(all_as_code)
    
    if create == 0 :
        TS += all_as_code
    
    if create == 1 :
        if DEBUG is 1 :
            print "creat="+str(creat)
            print "XS(total creat)="+str(XS)
        print "TS="+str(TS)

        assert TS != 0
        assert XS != 0

        print "score = (%s/%s)/(%s/%s)" % (str(all_as_code), str(TS), str(creat), str(XS))
        score = (all_as_code / TS) / (creat / XS)

        cell(tr, all_as_code)               # all as score
        cell(tr, (all_as_code / TS))        # code score
        if DEBUG != 0 :
            cell(tr, creat)                 # creat
            cell(tr, (creat / XS))          # creat score
        cell(tr, score)

def get_file_path(name):
    global REVIEW
    return REVIEW + "/" + MONTH + "/" + name + ".odt"

def all_odt(table, create) :
    global UDATA
    print "[all_odt] review path is %s" % REVIEW
    #for root, dirs, files in os.walk( REVIEW + "/" + MONTH ):
    #    for fn in files:
    #        single_odt(root+"/"+fn, get_name(fn), create, table)
    for name in UDATA:
        filepath = get_file_path(name)
        if not os.path.isfile(filepath):
            print "[all_odt] file %s not exist!" % filepath
            continue
        single_odt(filepath, name, create, table)

def header(table) :
    global DEBUG

    # title

    tr = TableRow(stylename=heighthigh)
    table.addElement(tr)

    cell(tr, "")
    cell(tr, "")
    cell(tr, "")
    cell(tr, "")
    cell(tr, MONTH + "研发中心 绩效评估表", bigtitle)

    # table header

    tr = TableRow()
    table.addElement(tr)
    
    cell(tr, "姓名", tableheader)
    cell(tr, "难度系数", tableheader)
    
    cell(tr, "自行发贴", tableheader)
    cell(tr, "热心回复", tableheader)
    cell(tr, "wiki文档", tableheader)
    cell(tr, "wiki代码", tableheader)
    cell(tr, "有效代码", tableheader)
    cell(tr, "bug贴", tableheader)
    cell(tr, "3月加成", tableheader)
    cell(tr, "组员贡献", tableheader)
    
    cell(tr, "绝对贡献", tableheader)
    cell(tr, "贡献占比", tableheader)
    if DEBUG != 0 :
        cell(tr, "creat", tableheader)
        cell(tr, "creat score", tableheader)
    cell(tr, "绩效系数", tableheader)

    cell(tr, "结果", tableheader)
    cell(tr, "备注", tableheader)
    
def footer(table) :

    # footer row 1

    tr = TableRow(stylename=heighthigh)
    table.addElement(tr)
    
    cell(tr, "部门主管\n签字", tablefooter)
    cell(tr, "")
    cell(tr, "")
    cell(tr, "")
    
    cell(tr, "总经理", tablefooter)
    cell(tr, "")
    cell(tr, "")
    cell(tr, "")

    cell(tr, "不参加考核", tablefooter)
    cell(tr, "")
    cell(tr, "")
    cell(tr, "")
    
    # footer row 2

    tr = TableRow(stylename=heighthigh)
    table.addElement(tr)

    cell(tr, "人力资源\n审核", tablefooter)
    cell(tr, "")
    cell(tr, "")
    cell(tr, "")

    cell(tr, "签字", tablefooter)
    cell(tr, "")
    cell(tr, "")
    cell(tr, "")

    cell(tr, "人员备注", tablefooter)
    cell(tr, "")
    cell(tr, "")
    cell(tr, "")

#
# main
#

def main():

  # Start the table, and describe the columns
  table = Table(name="jixiao")
  table.addElement(TableColumn(numbercolumnsrepeated=16,stylename=widthwide))
  
  # glue start
  get_udata()
  get_3m_data()
  get_total_creat()
  header(table)
  all_odt(table, 0)
  all_odt(table, 1)
  footer(table)
  # glue end
  
  doc.spreadsheet.addElement(table)

  # save to file

  if not os.path.isdir("output"):
    os.makedirs("output")

  # output/2015-06
  ods_path = "output/%s" % MONTH
  doc.save(ods_path, True) # odfpy auto add file prefix *.ods


if __name__ == '__main__':

  # Global variable

  MONTH = ""
  TS = 0.0
  XS = 0.0#xxdebug
  DEBUG = 0
  UDATA = {}

  # team member quality
  TMQ = 0.5
  
  # path
  REVIEW = "/home/chenyang/Mount/share/glue/review"
  if not os.path.isdir(REVIEW):
    REVIEW = "/mnt/share/art2/glue/review"

  #
  # Command line options parsing
  #

  #####################################################################
  # new in python 2.7
  #####################################################################
  #parser = argparse.ArgumentParser(description = "stat")
  #parser.add_argument('--month', action='store', dest='month',
  #                    help = "performance month, eg. 201507")
  #args = parser.parse_args()
  #arglist = args
  #####################################################################
  # old python
  #####################################################################
  parser = optparse.OptionParser()
  parser.add_option('--month', action='store', dest='month',
                      help = "performance month, eg. 201507")
  (options, args) = parser.parse_args()
  arglist = options
  #####################################################################

  # Using current month by defualt.
  if aarglist.month is None :
    print "No [month] param, start create performance of this month"
    MONTH = getDate().strftime("%Y%m")
  else:
    MONTH = arglist.month

  # Check time formate, 201507
  try:
    time.strptime(MONTH, "%Y%m")
  except:
    print "Time format error!"
    sys.exit(2)

  doc = OpenDocumentSpreadsheet()
  
  # Create a style for the table content. One we can modify
  # later in the word processor.
  tablecontents = Style(name="Table Contents", family="paragraph")
  tablecontents.addElement(ParagraphProperties(numberlines="false", linenumber="0"))
  doc.styles.addElement(tablecontents)
  
  # Create automatic styles for the column widths.
  # We want two different widths, one in inches, the other one in metric.
  # ODF Standard section 15.9.1
  widthwide = Style(name="Wwide", family="table-column")
  widthwide.addElement(TableColumnProperties(columnwidth="1.0in"))
  doc.automaticstyles.addElement(widthwide)
  
  # high height row
  heighthigh = Style(name="Hhigh", family="table-row")
  heighthigh.addElement(TableRowProperties(rowheight="1.2cm"))
  doc.automaticstyles.addElement(heighthigh)
  
  # one big title
  bigtitle = Style(name="Large title", family="table-cell")
  bigtitle.addElement(
      TextProperties(
          fontfamily="WenQuanYi Micro Hei",
          fontsize="15pt", fontsizeasian="15pt",
          fontweight="bold", fontweightasian="bold"
  ))
  doc.styles.addElement(bigtitle)
  
  # style for table header
  tableheader = Style(name="Table header", family="table-cell")
  tableheader.addElement(
      TextProperties(
          fontweight="bold", fontweightasian="bold"
  ))
  doc.styles.addElement(tableheader)
  
  # style for table footer
  tablefooter = Style(name="Large text", family="table-cell")
  tablefooter.addElement(
      TextProperties(
          fontfamily="WenQuanYi Micro Hei",
          fontsize="13pt", fontsizeasian="13pt",
          fontweight="bold", fontweightasian="bold"
  ))
  tablefooter.addElement(ParagraphProperties(textalign="center"))
  doc.styles.addElement(tablefooter)
  
  main()

#EOF
