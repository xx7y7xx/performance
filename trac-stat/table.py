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
import config
import wiki
import ticket
import xxutils
    

def TicketAndWikiWords(conn):
    table_filepath = config.TRAC_OUTPUT_PATH + "/table" + "/index.html"
    header = '''
    <html>\n
        <head>\n
            <title>统计wiki和ticket -- Superpolo Platform团队</title>\n
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />\n
        </head>\n
        <body>\n
            <h1>统计wiki和ticket字数</h1>\n
    '''
    body = ''
    
    # All wiki in one month.
    all_wiki = conn.cursor()
    all_wiki.execute("""select  distinct strftime('%Y', time/1000000, 'unixepoch', 'localtime') as y ,strftime('%m', time/1000000, 'unixepoch', 'localtime') as m 
from wiki
order by strftime('%Y', time/1000000, 'unixepoch', 'localtime') desc  ,strftime('%m', time/1000000, 'unixepoch', 'localtime') desc""")
    
    for year, month in all_wiki:
        # 2011|11
        xxutils.sp_debug('Processing wiki and ticket : ' + year + "-" + month)
        body += "<h2>" + year + "年" + month + "月 </h2> \n"
        body += '<table width=100% border=1>\n'
        body += '<tr>\n'
        body += '\t\t<td><b>姓名</b></td>\n'
        body += '\t\t<td><b>自行发帖字数</b></td>\n'
        body += '\t\t<td><b>自行发帖折合代码</b></td>\n'
        body += '\t\t<td><b>热心回复字数</b></td>\n'
        body += '\t\t<td><b>热心回复折合代码</b></td>\n'
        body += '\t\t<td><b>wiki整理</b></td>\n'
        body += '\t\t<td><b>wiki折合代码</b></td>\n'
        body += '</tr>\n'
        
        
        all_tickets = ticket.GetTicketStatByMonth(conn, year, month)
        all_tickets = ticket.GetAllCommentsInMonth(conn, year, month, all_tickets) # 将所有comments添加到相应的ticket中。
        users_list = []
        users_list = ticket.GetAllUsersInTrac(all_tickets)
        for user in users_list:
            body += '\t\t<tr>\n'
            body += '\t\t<td>'+user+'</td>\n'
            
        
            for all_ticket in config.REPLY_MY_TICKET:
                if all_ticket == year + month :
                    for my_ticket in config.REPLY_MY_TICKET[all_ticket]:
                        if my_ticket[0] == user: 
                            body += '\t\t<td>' + str(my_ticket[1]) + '</td>\n'
                            body += '\t\t<td>' + str(my_ticket[1] / 50 ) + '</td>\n'
                            
            for all_ticket in config.REPLY_OTHER_TICKET:
                if all_ticket == year + month :
                    for other_ticket in config.REPLY_OTHER_TICKET[all_ticket]:
                        if other_ticket[0] == user: 
                            body += '\t\t<td>' + str(other_ticket[1]) + '</td>\n'
                            body += '\t\t<td>' + str(other_ticket[1] / 40) + '</td>\n'
            
            
            wiki_month = wiki.GetWikiStatByMonth(conn, year, month)
            find = False
            for wiki_user, items in wiki_month.iteritems() :
                wiki_words = 0
               
                if wiki_user == user:
                    find = True
                    for name, item in items.iteritems() :
                        wiki_words += item["words"]
                    body += '\t\t<td>' + str(wiki_words) + '</td>\n'
                    body += '\t\t<td>' + str(wiki_words / 20) + '</td>\n'
            if not find:
               body += '\t\t<td>0</td>\n'
               body += '\t\t<td>0</td>\n'
                                    
                
            body += '\t\t</tr>\n'
                
        body += '</table>\n'
                
        
    all_wiki.close()      
   
    footer = '''
        <body>\n
    <html>\n
    '''
    f = open(table_filepath, 'w')
    f.write(header + body + footer)
    f.close()
    
