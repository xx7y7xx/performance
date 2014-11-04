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

def calc_perf(odt_dir):
    """Calculate all the users' performance data."""
    pf = {}

    # prepare contrib data
    all_work = 0
    uname_list = get_uname_list()
    udata_list = get_udata_list()
    for uname in uname_list:
        fpath = odt_dir + "/" + uname + ".odt"
        if not os.path.isfile(fpath):
            continue

        pf[uname] = {}

        contrib = parse_odt(fpath)

        is_3m = ( uname in get_3m_uname_list() )
        pf[uname]['money'] = udata_list[uname]['qian']
        pf[uname]['quality'] = quality = udata_list[uname]['quality']

        # every single contrib
        pf[uname]['self_ticket'] = self_ticket = contrib[0]
        pf[uname]['other_ticket'] = other_ticket = contrib[1]
        pf[uname]['wiki'] = wiki = contrib[2]
        pf[uname]['wiki_code'] = wiki_code = contrib[3]
        pf[uname]['code'] = code = contrib[4]
        pf[uname]['bug_ticket'] = bug_ticket = contrib[5]
        pf[uname]['boost'] = boost = contrib[6]
        pf[uname]['member'] = member = contrib[7]

        single_work = float(code*quality + boost*10*is_3m + bug_ticket*20 + wiki_code/100 + wiki/20 + self_ticket/50 + other_ticket/40 + member/10)
        all_work += single_work
        pf[uname]['amount_of_work'] = single_work

    for uname in pf:
        pf[uname]['score'] = (pf[uname]['amount_of_work'] / all_work) / (pf[uname]['money'] / get_total_money())
    return pf

def get_odt_dir():
    """Get the dir contains odt files
    usally this is a samba server mounted on local machine.
    """
    global REVIEW
    return REVIEW + "/" + str(getDate().year) + "-" + getDate().strftime("%m") 

def get_total_money():
    """Sum all users' money"""
    udata_list = get_udata_list()
    tm = 0
    for n,d in udata_list.items() :
        #if DEBUG is 1 :
        #    print "[get_total_money] name : '"+n+"'"
        #    print "[get_total_money] money : '"+str(d['qian'])+"'"
        tm += d['qian']
    return tm

def get_udata_list():
    from cfg import UDATA
    return UDATA

def get_uname_list():
    """Get user list from glue trac."""
    try:
        username = "ci"
        password = "sp12345678"
        top_level_url = "http://glue.spolo.org"
        url = "http://glue.spolo.org/trac/glue/wiki/%E5%BC%80%E5%8F%91%E4%BA%BA%E5%91%98%E4%BF%A1%E6%81%AF?format=txt"

        # create a password manager
        password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        
        # Add the username and password.
        # If we knew the realm, we could use it instead of None.
        password_mgr.add_password(None, top_level_url, username, password)
        
        handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        
        # create "opener" (OpenerDirector instance)
        opener = urllib2.build_opener(handler)
        
        # use the opener to fetch a URL
        response = opener.open(url)

    except HTTPError as e:
        msg = "URL : %s\n" % url
        msg += 'Server return code : %s' % e.code
        print(msg)
    #except e:
    #    print(('Unexpected exception thrown:', e))

    raw_data = response.read().decode('utf-8')
    #print raw_data

    # get real developer
    ret = []
    for line in raw_data.splitlines():
        # find all developer from email address.
        m = re.search(r"(\w+)@spolo.org", line)
        if m:
            name = m.group(1)

            # not developer.
            if name in ["liwei", "hanlu", "changyushan", "peizhelun", "tangying"]:
                continue

            ret.append(name)

    return ret

def create_ods(filename):
    doc = OpenDocumentSpreadsheet()
    #doc.spreadsheet.addElement(table)
    #doc.save(filename, True) # add "ods" as suffix
    doc.save(filename) # not add "ods" as suffix

def get_3m_uname_list(fname = "boost.txt"):
    with open(fname) as f:
        #ul = f.readlines()
        ul = f.read().splitlines()
    return ul

#EOF
