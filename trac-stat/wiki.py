#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

#/**************************************************************************
# *
# *  This file is part of the UGE(Uniform Game Engine).
# *  Copyright (C) by SanPolo Co.Ltd. 
# *  All rights reserved.
# *
# *  See http://uge.spolo.org/ for more information.
# *
# *  SanPolo Co.Ltd
# *  http://uge.spolo.org/  sales@spolo.org uge-support@spolo.org
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
        
        # 忽略一些用户，比如离职。
        if author not in config.SPP_USERS:
            continue
        
        row = {}
        row["name"] = name
        row["version"] = version
        row["author"] = author
        row["text"] = text
        
        if version == 1 :
            diff = wikiwc(text)

            # exclude personal wiki page, and wiki code page.
            if xxutils.IsExcludeWiki(name) or xxutils.IsWikiSourcePage(name):
                row["change"] = 0
            else:
                row["change"] = diff

        else :
            #需要找到前一个版本比较
            lastversion = version - 1
            
            t = (name, lastversion)
            lastmodify_wiki = conn.cursor()
            lastmodify_wiki.execute("""select name,version,author,length(text),text  from wiki where name =? and version=?
            """, t)
            
            r = lastmodify_wiki.fetchone()
            
            if len(r) > 0 :
                lasttext = r[4] # text
            else :
                lasttext = ""
            
            diff = wikiwc(lasttext, text)

            # exclude personal wiki page, and wiki code page.
            if xxutils.IsExcludeWiki(name) or xxutils.IsWikiSourcePage(name):
                row["change"] = 0
            else:
                row["change"] = diff
            
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
                output += "<td><a target=_blank href='" + config.TRAC_URL + "/wiki/" + name + "'>"  + name + "</a></td>\n"
                
                output += "<td>\n"
                versions = str(item["versions"]).split(";")
                for version in versions :
                    version = int(version)
                    if version != 1 :
                        output += "&nbsp;<a target=_blank href='" + config.TRAC_URL + "/wiki/" + name + "?action=diff&version=" + str(version) + "&old_version=" + str(version - 1) + "'>V"  + str(version) + "</a>"
                
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
                output += "<tr><td><a target=_blank href='" + config.TRAC_URL + "/wiki/" + name + "'>" + name + "</a></td><td>"
                
                versions = str(item["versions"]).split(";")
                for version in versions :
                    version = int(version)
                    if version != 1 :
                        output += "&nbsp; <a target=_blank href='" + config.TRAC_URL + "/wiki/" + name + "?action=diff&version=" + str(version) + "&old_version=" + str(version - 1) + "'>V"  + str(version) + "</a>"
                
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
    
    index += '''<script type="text/javascript" src="http://ajax.googleapis.com/ajax/static/modules/gviz/1.0/chart.js">
    {
        "dataSourceUrl":"http://docs.google.com/a/masols.com/spreadsheet/tq?key=0AqwnDQvWEnMgdFlxUXo3VVU4YmRJR0NDSTZMWmZPWVE&transpose=1&headers=1&range=A1%3AE18&gid=0&pub=1",
        "options":{
            "vAxes":[{
                "title":"\u5b57\u6570",
                "minValue":null,
                "viewWindowMode":"pretty",
                "viewWindow":{"min":null,"max":null},
                "maxValue":null
            },{
                "viewWindowMode":"pretty",
                "viewWindow":{}
            }],
            "reverseCategories":false,
            "title":"Wiki\u5b57\u6570\u8d8b\u52bf\u56fe",
            "interpolateNulls":false,
            "pointSize":"7",
            "backgroundColor":"#FFFFFF",
            "legend":"right",
            "lineWidth":2,
            "logScale":false,
            "hAxis":{
                "maxAlternations":1
            },
            "hasLabelsColumn":true,
            "reverseAxis":false,
            "width":600,
            "height":525
        },
        "state":{},
        "view":"{\"columns\":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]}",
        "chartType":"LineChart",
        "chartName":"Chart 1"
    }
    </script>'''
    index += "<table width=30% border=1>\n"
    index += "<tr><td>姓名</td><td>字数</tr>\n"
    for user, word in sort :
        index += "<tr><td><a href='" + current + "#" + user + "'> " + user + "</a> </td><td> " + str(word) + "</tr>\n"
    index += "</table>"
    
    pathname = config.TRAC_OUTPUT_PATH + "/wiki" + "/" + year + month + ".html"
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
    
    pathname = config.TRAC_OUTPUT_PATH + "/wiki" + "/index.html"
    
    f = open(pathname, 'w')
    f.write(index)
    f.close()

# count word in wiki text
def wikiwc(rev1, rev2 = None):
    # only one revision
    if rev2 == None :
        # remove "{{{...}}}"
        content = xxutils.sub_code_block(rev1)

        #content = xxutils.rm_whitespace(content)
        #content = xxutils.rm_linebreak(content)
        return xxutils.cws(content)
    # has previous revision.
    else :
        # remove "{{{...}}}", then diff.
        rev1_content = xxutils.sub_code_block(rev1)
        rev2_content = xxutils.sub_code_block(rev2)

        diff = xxutils.find_diff_code_lines(rev1_content, rev2_content)

        return xxutils.cws(diff)

