#!/usr/bin/python2.7
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

from datetime import datetime
import config
import xxutils
import re

def WikiAddItem(wiki, item) :
    if not item["author"] in wiki :
        wiki[ item["author"] ] = {}
   
    if not item["name"] in wiki[ item["author"] ] :
        wiki[ item["author"] ][ item["name"] ] = {}
        wiki[ item["author"] ][ item["name"] ]["words"] = item["change"]
        wiki[ item["author"] ][ item["name"] ]["versions"] = item["version"]
        wiki[ item["author"] ][ item["name"] ]["times"] = 1
        if item["version"] == 1 :
            wiki[ item["author"] ][ item["name"] ]["create"] = 1
        else :
            wiki[ item["author"] ][ item["name"] ]["create"] = 0
    else :
        wiki[ item["author"] ][ item["name"] ]["words"] += item["change"]
        wiki[ item["author"] ][ item["name"] ]["versions"] = str(wiki[ item["author"] ][ item["name"] ]["versions"]) + ";" + str(item["version"])
        wiki[ item["author"] ][ item["name"] ]["times"] += 1
        if item["version"] == 1 or wiki[ item["author"] ][ item["name"] ]["create"] == 1 :
            wiki[ item["author"] ][ item["name"] ]["create"] = 1
   
    return wiki

def GetWikiStatByMonth(conn, year, month) :
    t = (year, month, )

    month_wiki = conn.cursor()
    month_wiki.execute("""select name,version,author,length(text),text, strftime('%Y', time/1000000, 'unixepoch', 'localtime') as y ,strftime('%m', time/1000000, 'unixepoch', 'localtime') as m
from wiki
where strftime('%Y', time/1000000, 'unixepoch', 'localtime') = ? and strftime('%m', time/1000000, 'unixepoch', 'localtime')=?""", t)
   
    wiki = {}
    for name, version, author, text_len, text, year, month in month_wiki :
       
        row = {}
        row["name"] = name
        row["version"] = version
        row["author"] = author
        row["text"] = text

        if not xxutils.IsWikiSourcePage(name):
            continue

        if version == 1 :
            row["change"] = xxutils.wikicc(text)
        else :
            #需要找到前一个版本比较
            lastversion = version - 1
           
            t = (name, lastversion)
            lastmodify_wiki = conn.cursor()
            lastmodify_wiki.execute("""select name,version,author,length(text),text  from wiki where name =? and version=?
            """, t)
           
            r = lastmodify_wiki.fetchone()
           
            if len(r) > 0 :
                lasttext = r[4] # r['text']
            else :
                lasttext = ""

            row["change"] = xxutils.wikicc(lasttext, text)
           
            lastmodify_wiki.close()
       
        wiki = WikiAddItem(wiki, row);

    month_wiki.close()
   
    return wiki

##
# @brief write data to pages
##
def WikiWritePage(conn, year, month) :
    wiki = GetWikiStatByMonth(conn, year, month)
    title = year + "年" + month + "月 Wiki统计"
    index = ""
    output = ""
    header = "<html>\n"
    header += "\t<head>\n"
    header += "\t\t<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\" />\n"
    header += "\t\t<title>" + title + "</title>\n\t</head>\n\t<body>\n<h1>" + title + "</h1>\n"
   
    not_sort = {}
   
    for user, items in wiki.iteritems() :
       
        # 当月的总的wiki字数
        words = 0
        wikitext = "" # show this in <texteare>
       
        output += "<h2><span id=" + user + "><font color=red>" + user + "</font></span></h2>\n"
        output += "<h3>创建</h3>\n"
        output += "<table width='100%' border=1>\n<tr><td>标题</td><td>修改记录</td><td>操作次数</td><td>字数统计</td></tr>\n"
        wikitext += "=== 本月创建Wiki列表\n"
       
        for name, item in items.iteritems() :
       
            if item["create"] == 1 :
           
                output += "<tr>\n"
                output += "<td><a target=_blank href='" + config.TRAC_WIKI_URL + "/" + name + "'>"  + name + "</a></td>\n"#xxdebug
               
                output += "<td>\n"
                versions = str(item["versions"]).split(";")
                for version in versions :
                    version = int(version)
                    if version != 1 :
                        output += "&nbsp;<a target=_blank href='" + config.TRAC_WIKI_URL + "/" + name + "?action=diff&version=" + str(version) + "&old_version=" + str(version - 1) + "'>V"  + str(version) + "</a>"#xxdebug
               
                output += "</td>\n"
                output += "<td>" + str(item["times"]) + "</td>\n"
                output += "<td>" + str(item["words"]) + "</td>\n"
                output += "</tr>\n"
                words += item["words"]
               
                wikitext += "|| wiki:" + name + " ||\n"
       
        output += "</table>\n"
        output += "<h3>修改</h3>\n"
        output += "<table width='100%' border=1><tr><td>标题</td><td>修改记录</td><td>操作次数</td><td>字数统计</td></tr>\n "
        wikitext += "=== 本月修改Wiki列表\n"
       
        for name, item in items.iteritems() :
           
            if item["create"] == 0 :
                output += "<tr><td><a target=_blank href='" + config.TRAC_WIKI_URL + "/" + name + "'>" + name + "</a></td><td>"#xxdebug
               
                versions = str(item["versions"]).split(";")
                for version in versions :
                    version = int(version)
                    if version != 1 :
                        output += "&nbsp; <a target=_blank href='" + config.TRAC_WIKI_URL + "/" + name + "?action=diff&version=" + str(version) + "&old_version=" + str(version - 1) + "'>V"  + str(version) + "</a>"#xxdebug
               
                output += "</td>\n<td>" + str(item["times"]) + "</td>\n<td>"
                output += str(item["words"]) + "</td>\n</tr>\n"
                words += item["words"]
               
                wikitext += "|| wiki:" + name + " ||\n"
       
        output += "</table>\n"
        output += "<h3>字数统计：" + str(words) + "</h3>\n"
       
        wikitext += "=== 统计信息\n"
        wikitext += "|| 字数统计 ||\n" + "|| " + str(words) + " ||\n"
       
        # Copy this to your ticket.
        output += "<h3>复制如下内容，替换自评贴中的“{Wiki内容列表}”</h3>\n<textarea cols=100 rows=10>\n" + wikitext + "\n</textarea>\n<br><br><hr>"
       
        not_sort[ user ] = words
   
   
    output += "</body></html>"

    sort = xxutils.asort( not_sort )

    current = year + month + ".html"
   
    index += "<table width=30% border=1>\n"
    index += "<tr><td>姓名</td><td>字数</tr>\n"
    for user, word in sort :
        index += "<tr><td><a href='" + current + "#" + user + "'> " + user + "</a> </td><td> " + str(word) + "</tr>\n"
    index += "</table>"
   
    pathname = config.TRAC_OUTPUT_PATH + "/code/" + year + month + ".html"#xxdebug
    f = open(pathname, 'w')
    f.write(header + index + output)
    f.close()

    return index

##
# @brief Query database for all the month info in Trac Wiki.
##
def WikiDealAllMonth(conn):
   
    index = "<html><head><title>Wiki统计</title>  <meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\" /></head><body><h1>Wiki统计</h1>"
    index += "<i>Generated: " + str(datetime.now()) + "</i>"
   
    # All wiki in one month.
    all_wiki = conn.cursor()
    all_wiki.execute("""select  distinct strftime('%Y', time/1000000, 'unixepoch', 'localtime') as y ,strftime('%m', time/1000000, 'unixepoch', 'localtime') as m
from wiki
order by strftime('%Y', time/1000000, 'unixepoch', 'localtime') desc  ,strftime('%m', time/1000000, 'unixepoch', 'localtime') desc""")
   
    for year, month in all_wiki:
        # 2011|11
        index += "<h2><a target=_blank href='" + year + month + ".html'>" + year + "年" + month + "月 </a></h2> \n"
        index += WikiWritePage(conn, year , month)
   
    all_wiki.close()

    index += "</body></html>"

    #xxdebug
    pathname = config.TRAC_OUTPUT_PATH + "/code/index.html"
   
    f = open(pathname, 'w')
    f.write(index)
    f.close()
