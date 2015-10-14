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

##
# @brief `oldvalue`字段中保存的comment id有点特殊
# 比如“3.7”说明是在7楼回复的内容，并且reply to 3楼。
##
def GetCommentID(id) :
	tmp = (str(id)).split(".")
	if len(tmp) == 2 :
		return tmp[1]
	else :
		return tmp[0]

##
# @brief 获取以id为索引的所有帖子。
# {
#   "123" : {
#     "owner" : "caobin",
#     "reporter" : "chenyang",
#     "type" : "task",
#     "comment" : {}
#   },
#   "321" : {},
#   "456" : {}
# }
##
def AddItem2Ticket(ticket, item) :
	if not item["id"] in ticket :
		ticket[ item["id"] ] = {}
		ticket[ item["id"] ]["words"] = 0
	
	ticket[ item["id"] ]["type"]        = item["type"]
	ticket[ item["id"] ]["component"]   = item["component"]
	ticket[ item["id"] ]["create_time"] = item["create_time"]
	ticket[ item["id"] ]["name"]        = item["name"]
	ticket[ item["id"] ]["description"] = item["description"]
	ticket[ item["id"] ]["owner"]       = item["owner"]
	ticket[ item["id"] ]["reporter"]    = item["reporter"]
	ticket[ item["id"] ]["comment"]     = {}
	
	return ticket

##
# @brief 
# {
#   "123" : {
#     "owner" : "caobin",
#     "reporter" : "chenyang",
#     "author" : "masol" # 发表回帖的人
#   },
#   "321" : {},
#   "456" : {}
# }
##
def AddItem2Comment(comment, item) :
	if not item["id"] in comment :
		comment[ item["id"] ] = {}
		comment[ item["id"] ]["words"] = 0
	
	comment[ item["id"] ]["words"] += item["change"]
	
	comment[ item["id"] ]["name"]     = item["name"]
	comment[ item["id"] ]["author"]   = item["author"]
	comment[ item["id"] ]["owner"]    = item["owner"]
	comment[ item["id"] ]["reporter"] = item["reporter"]
	
	return comment

def GetAllUsersInTrac(all_tickets) :
  """分别遍历所有ticket和所有comment从而形成一个用户列表。

  Not "ALL" tickets, but tickets in selected month.
  只要用户出现在如下情况中，那么本函数就会将这个人（someone）记录在列表中。
  * owner = someone
  * reporter = someone
  * author = someone （回复别人的帖子的时候，那个回帖的人叫做author）

  Args:
    all_tickets: 

  Returns:
    A list of users

  Raises:
    ??
  """
	users_list = []
	for ticket_id, ticket in all_tickets.iteritems() :
		# 忽略一些用户，比如离职。
		if ticket["reporter"] not in users_list :
			users_list.append(ticket["reporter"])
		if ticket["owner"] not in users_list :
			users_list.append(ticket["owner"])
		
		# 处理回帖的用户，因为有些用户可能只回帖不创建帖子。
		for comment_id, comment in ticket["comment"].iteritems() :
			# 忽略一些用户，比如离职。
			if comment["author"] not in users_list :
				users_list.append(comment["author"])
	
	return users_list

##
# @brief Get all tickets (w/o comment) in ONE month.
##
def GetTicketStatByMonth(conn, year, month):
	
	ticket = {}
	
	t = (year, month, )

	# All tickets in one month.
	all_ticket = conn.cursor()
	all_ticket.execute('''
SELECT
	id, type, time, component, owner, reporter, version, summary, description,
	strftime('%Y', time/1000000, 'unixepoch', 'localtime') as year,
	strftime('%m', time/1000000, 'unixepoch', 'localtime') as month,
	strftime('%Y-%m-%d %H:%M:%S', time/1000000, 'unixepoch', 'localtime') as datetime
FROM
	ticket
WHERE
	strftime('%Y', time/1000000, 'unixepoch', 'localtime') = ? and
	strftime('%m', time/1000000, 'unixepoch', 'localtime') = ?
ORDER BY
	time''', t)

	for ticket_id, type, time, component, owner, reporter, version, summary, description, year, month, datetime in all_ticket:
		# (37, 1320131640946928L, u'peiluyi', u'peiluyi', u'', u'\u65b0\u5458\u5de5\u57f9\u8bad\u7b2c\u4e00\u5929', u'\u8ba4\u8bc6 SuperPolo \u56e2\u961f\r\n\u719f\u6089 SuperPolo Platform \r\n\u4e86\u89e3 UGE \u7684\u6982\u5ff5 ', u'2011', u'11')
		item = {}
		item["id"] = str(ticket_id)
		item["type"] = type
		item["create_time"] = datetime
		item["component"] = component
		item["owner"] = owner
		item["reporter"] = reporter
		item["name"] = summary
		item["description"] = description
		
		ticket = AddItem2Ticket(ticket, item)
	
	all_ticket.close()
	
	return ticket

##
# @brief Get all comments in ONE month.
##
def GetCommentStatByMonth(conn, year, month):
	
	comments = {}
	
	t = (year, month, )
	
	# All comments in one month.
	all_comment = conn.cursor()
	all_comment.execute('''
SELECT
	ticket, author, field, oldvalue, newvalue,
	strftime('%Y', ticket_change.time/1000000, 'unixepoch', 'localtime') as year,
	strftime('%m', ticket_change.time/1000000, 'unixepoch', 'localtime') as month,
	ticket.id, ticket.type, ticket.component, ticket.owner, ticket.reporter, ticket.summary
FROM
	ticket_change, ticket
WHERE
	ticket_change.ticket = ticket.id and
	field = 'comment' and
	strftime('%Y', ticket_change.time/1000000, 'unixepoch', 'localtime') = ? and
	strftime('%m', ticket_change.time/1000000, 'unixepoch', 'localtime') = ?
ORDER BY
	ticket_change.time
	''', t)

	for	ticket_change_ticket, ticket_change_author, ticket_change_field, \
	ticket_change_oldvalue, ticket_change_newvalue, ticket_change_year, \
	ticket_change_month, ticket_id, ticket_type, ticket_component, ticket_owner, ticket_reporter, \
	ticket_summary in all_comment:
		# (85, u'chenyang', u'comment', u'11', u'\u53c2\u7167diff:default/trunk/thirdparty/libv8-convert-20110729@43:44', u'2011', u'11', 85, u'liwei', u'\u51c6\u5907windows\u5de5\u4f5c\u73af\u5883')
		item = {}
		item["id"] = str(ticket_change_ticket)
		item["type"] = ticket_type
		item["component"] = ticket_component
		item["author"] = ticket_change_author
		item["reporter"] = ticket_reporter
		item["owner"] = ticket_owner
		item["name"] = ticket_summary
		
		item["change"] = xxutils.ticket_wc(ticket_change_newvalue)
		
		comments = AddItem2Comment(comments, item)
	
	all_comment.close()
	
	return comments

##
# @brief Get all comments in ONE month.
# @details To replace `GetCommentStatByMonth` function
# The return type (in JSON format), show as:
# {
#   "123" : {
#     "reporter" : "chenyang",
#     "owner" : "caobin",
#     "comment" : {
#       "1" : {
#         "author" : "masol" # 发表回帖的人
#         "content" : "..." # 发帖的最新内容。
#       },
#       "2" : {
#         "author" : "chenyang"
#         "content" : "..."
#       }
#     }
#   },
#   "321" : {},
#   "456" : {}
# }
##
def GetAllCommentsInMonth(conn, year, month, all_tickets):
	
	t = (year, month, )
	
	# All comments in one month.
	all_comment = conn.cursor()
	all_comment.execute('''
SELECT
	ticket, author, field, oldvalue, newvalue,
	strftime('%Y', ticket_change.time/1000000, 'unixepoch', 'localtime') as year,
	strftime('%m', ticket_change.time/1000000, 'unixepoch', 'localtime') as month,
	ticket.id, ticket.type, ticket.time, ticket.component, ticket.owner, ticket.reporter, ticket.summary, ticket.description,
	strftime('%Y-%m-%d %H:%M:%S', ticket.time/1000000, 'unixepoch', 'localtime') as ticket_datetime
FROM
	ticket_change, ticket
WHERE
	ticket_change.ticket = ticket.id and
	field = 'comment' and
	strftime('%Y', ticket_change.time/1000000, 'unixepoch', 'localtime') = ? and
	strftime('%m', ticket_change.time/1000000, 'unixepoch', 'localtime') = ?
ORDER BY
	ticket_change.time
	''', t)

	for	ticket_change_ticket, ticket_change_author, ticket_change_field, \
	ticket_change_oldvalue, ticket_change_newvalue, ticket_change_year, \
	ticket_change_month, ticket_id, ticket_type, ticket_time, ticket_component, ticket_owner, ticket_reporter, \
	ticket_summary, ticket_description, ticket_datetime in all_comment:
		# (85, u'chenyang', u'comment', u'11', u'\u53c2\u7167diff:default/trunk/thirdparty/libv8-convert-20110729@43:44', u'2011', u'11', 85, u'liwei', u'\u51c6\u5907windows\u5de5\u4f5c\u73af\u5883')
		item = {}
		item["ticket_id"] = str(ticket_change_ticket)
		item["type"] = ticket_type
		item["component"] = ticket_component
		item["create_time"] = ticket_time # 创建帖子的时间
		item["comment_create_time"] = ticket_datetime # 添加回复的时间
		item["author"] = ticket_change_author
		item["reporter"] = ticket_reporter
		item["owner"] = ticket_owner
		item["name"] = ticket_summary
		item["description"] = ticket_description
		item["comment_content"] = ticket_change_newvalue
		
		# 回复某一楼的帖子的comment id有点奇怪，比如在4楼回复1楼的帖子，
		# 则comment id在db中的field字段中保存为text格式的“1.4”，需要特殊对待。
		item["comment_id"] = GetCommentID(ticket_change_oldvalue)
		
		item["change"] = xxutils.ticket_wc(ticket_change_newvalue)
		
		# 如果该comment对应的ticket没有出现在dict中，创建之。
		if not item["ticket_id"] in all_tickets :
			all_tickets[ item["ticket_id"] ] = {}
			all_tickets[ item["ticket_id"] ]["reporter"] = item["reporter"]
			all_tickets[ item["ticket_id"] ]["owner"] = item["owner"]
			all_tickets[ item["ticket_id"] ]["type"] = item["type"]
			all_tickets[ item["ticket_id"] ]["component"] = item["component"]
			all_tickets[ item["ticket_id"] ]["create_time"] = item["create_time"]
			all_tickets[ item["ticket_id"] ]["name"] = item["name"]
			all_tickets[ item["ticket_id"] ]["description"] = item["description"]
			all_tickets[ item["ticket_id"] ]["words"] = 0
			all_tickets[ item["ticket_id"] ]["comment"] = {}
		
		# 将该comment添加到对应ticket下
		all_tickets[ item["ticket_id"] ]["comment"][ item["comment_id"] ] = {}
		all_tickets[ item["ticket_id"] ]["comment"][ item["comment_id"] ]["author"] = item["author"]
		all_tickets[ item["ticket_id"] ]["comment"][ item["comment_id"] ]["content"] = item["comment_content"]
		all_tickets[ item["ticket_id"] ]["comment"][ item["comment_id"] ]["time"] = item["comment_create_time"]
	
	all_comment.close()
	
	return all_tickets

###
def TicketDealOneMonth(conn, year, month):
	
	xxutils.sp_debug("Processing month : " + year + "-" + month)
	
	all_tickets = GetTicketStatByMonth(conn, year, month)
	all_comments = GetCommentStatByMonth(conn, year, month)
	all_tickets = GetAllCommentsInMonth(conn, year, month, all_tickets) # 将所有comments添加到相应的ticket中。

	title = year + "年" + month + "月 Ticket统计"
	header = "<html>\n\
\t<head>\n\
\t\t<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\" />\n\
\t\t<title>" + title + "</title>\n\
\t\t<style>\n\
\t\t  tr { background-color: #DDDDDD}\n\
\t\t  .initial { background-color: #DDDDDD; color:#000000 }\n\
\t\t  .normal { background-color: #DDDDDD }\n\
\t\t  .highlight { background-color: #8888FF }\n\
\t\t</style>\n\
\t</head>\n\
\t<body>\n"
	header += "\t\t<h1 id=\"top\">" + title + "</h1>\n"
	
	output = ""
	index = ""
	
	no_sort_ticket = {}
	no_sort_ticket_count_other = {}
	no_sort_reply_in_my_ticket = {} # 回复自己的帖子
	no_sort_warmhearted_reply = {} # 热心回复
	
	# 分别遍历所有ticket和所有comment从而形成一个用户列表。
	users_list = []
	users_list = GetAllUsersInTrac(all_tickets)
	
	# 打印debug信息：列出所有开发人员。
	xxutils.sp_debug("Active developer in this month : " + str(users_list))
	
	# 统计每个开发者的帖子/回复的个数/字数。
	for user in users_list :
		
		# new ticket for myself
		count = 0 # count of ticket
		words = 0
		times = 0 # change times of ticket, include one description and many comments.
		# new ticket (type is task only) for other, means you are his leader.
		count_other = 0
		words_other = 0
		times_other = 0
		
		# 计算发帖个数和字数，包括。
		for ticket_id, item in all_tickets.iteritems() :
			# 自己的帖子
			if item["owner"] == user :
				# 自己开贴。
				if item["reporter"] == user :
					count += 1
					words += item["words"]
				# 别人开贴。
				#else :
				
			# 别人的帖子，自己开贴。
			if item["owner"] != user and item["reporter"] == user :
				words += item["words"]
				# 只计算给别人发的task贴。
				# task in glue trac named "1_task" and "2_task".
				if item["type"] == "task" or item["type"] == "1_task" or item["type"] == "2_task" :
					count_other += 1
		
		# 计算发回复的个数和字数。
		for ticket_id, item in all_comments.iteritems() :
			if item["author"] != user :
				continue
			# 回复owner是自己的帖子。
			if item["owner"] == user :
				words += item["words"]
			# 回复owner不是自己的帖子，属于热心回复。
			else :
				words_other += item["words"]
		
		no_sort_ticket[user] = count
		no_sort_ticket_count_other[user] = count_other
	
	for user in users_list :
	
		xxutils.sp_debug("Processing developer : " + user)
		
		no_sort_warmhearted_reply[user] = 0
		no_sort_reply_in_my_ticket[user] = 0
		
		wikitext = ""
		output += "<h2><span id=" + user + "><font color=red>  " + user + "</font></span></h2>\n"
		
		# Show details ticket list, these tickets are mine.
		output += "<h3><span id=\"" + user + "-create4myself\">我的帖子</span></h3>\n"
		output += "<table width='100%' border=1><tr><th width=\"5%\">Ticket</th><th width=\"30%\">Summary</th><th width=\"5%\">Reporter</th><th width=\"5%\">Owner</th><th>我的回复</th><th width=\"10%\">我的回复总字数</th></tr>\n"
		wikitext += "=== 我的帖子 ===\n"
		for ticket_id, ticket in all_tickets.iteritems() :
			# 略过其他人的帖子。
			if ticket["owner"] != user :
				continue
			
			# 统计该用户所有回复。
			coment_id_list = "" # 保存该用户在该ticket中所有comment id，"1,3,4"
			comments_word_count = 0
			for comment_id, comment in ticket["comment"].iteritems() :
				# 略过别人的回复。
				if comment["author"] != user :
					continue
				
				comment_word_count = xxutils.ticket_wc(comment["content"])
				comments_word_count += comment_word_count
				coment_id_list += xxutils.createCommentLink(
					config.TRAC_URL,
					ticket_id, # URL帖子号部分
					comment_id, # URL的comment号部分。
					comment_id + "楼(" + str(comment_word_count) + "字)" # 链接名称
				)
				coment_id_list += ", "
			
			output += "<tr onmouseover=\"this.className='highlight'\" onmouseout=\"this.className='normal'\">\n"
			output += "<td>" + xxutils.createTicketLink(config.TRAC_URL, ticket_id, "#"+ticket_id) + "</td>\n"
			output += "<td>" + xxutils.createTicketLink(config.TRAC_URL, ticket_id, ticket["name"]) + "</td>\n"
			output += "<td>" + ticket["reporter"] + "</td>\n"
			output += "<td>" + ticket["owner"] + "</td>\n"
			output += "<td>" + coment_id_list + "</td>\n"
			output += "<td>" + str(comments_word_count) + "</td>\n"
			output += "</tr>\n"
			wikitext += "|| #" + ticket_id + " || " + '[#' + ticket_id + ' "' + ticket["name"] + '"] ||' + "\n"
			
			# 计算用户在自己帖子中的回复字数。
			no_sort_reply_in_my_ticket[user] += comments_word_count
			
		output += "</table>\n"
		
		# Show details ticket list, these tickets are created by myself, and for others.
		# And the ticket type must be "task", means you are his leader.
		output += "<h3><span id=\"" + user + "-create4others\">为别人创建任务贴</span></h3>\n"
		output += "<table width='100%' border=1>\n<tr>\n<th width=\"5%\">Ticket</th><th>Summary</th><th width=\"5%\">Reporter</th><th width=\"5%\">Owner</th><th width=\"10%\">Description字数</th>\n</tr>\n"
		wikitext += "=== 为别人创建任务贴 ===\n"
		for ticket_id, ticket in all_tickets.iteritems() :
			if ticket["reporter"] == user and ticket["owner"] != user :
				if ticket["type"] != "task" :
					continue
				words_of_summary_and_description = xxutils.ticket_wc(ticket["name"] + config.EOL + ticket["description"])
				output += "<tr onmouseover=\"this.className='highlight'\" onmouseout=\"this.className='normal'\">\n"
				output += "<td>" + xxutils.createTicketLink(config.TRAC_URL, ticket_id, "#"+ticket_id) + "</td>\n"
				output += "<td>" + xxutils.createTicketLink(config.TRAC_URL, ticket_id, ticket["name"]) + "</td>\n"
				output += "<td>" + str(ticket["reporter"]) + "</td>\n"
				output += "<td>" + str(ticket["owner"]) + "</td>\n"
				output += "<td>" + str(words_of_summary_and_description) + "</td>\n"
				output += "</tr>\n"
				wikitext += "|| #" + ticket_id + " || " + '[#' + ticket_id + ' "' + ticket["name"] + '"] ||' + "\n"
		output += "</table>\n"
		
		output += "<h3>热心回复</h3>\n"
		wikitext += "=== 热心回复 ===\n"
		output += "<table width='100%' border=1><tr><th width=\"5%\">Ticket</th><th width=\"30%\">Summary</th><th width=\"5%\">Reporter</th><th width=\"5%\">Owner</th><th>我的回复</th><th width=\"10%\">我的回复总字数</th></tr>\n "
		for ticket_id, ticket in all_tickets.iteritems() :
			# 略过自己的帖子。
			if ticket["owner"] == user :
				continue
			
			#xxutils.sp_debug("Processing ticket : " + ticket_id)##大大的拖慢运行时间，调试需谨慎。
			
			found_user = False # 记录用户是否在这个帖子中回复了
			
			coment_id_list = "" # 保存该用户在该ticket中所有comment id，"1,3,4"
			comments_word_count = 0
			
			for comment_id, comment in ticket["comment"].iteritems() :
				# 略过别人的回复。
				if comment["author"] != user :
					continue
				
				comment_word_count = xxutils.ticket_wc(comment["content"])
				comments_word_count += comment_word_count
				coment_id_list += xxutils.createCommentLink(
					config.TRAC_URL,
					ticket_id, # URL帖子号部分
					comment_id, # URL的comment号部分。
					comment_id + "楼(" + str(comment_word_count) + "字)" # 链接名称
				)
				coment_id_list += ", "
				
				found_user = True
			
			# 用户没有在这个帖子中回复过。
			if found_user == False :
				continue
			
			# 构建该ticket的行。
			output += "<tr onmouseover=\"this.className='highlight'\" onmouseout=\"this.className='normal'\">\n"
			output += "<td>" + xxutils.createTicketLink(config.TRAC_URL, ticket_id, "#"+ticket_id) + "</td>\n"
			output += "<td>" + xxutils.createTicketLink(config.TRAC_URL, ticket_id, ticket["name"]) + "</td>\n"
			output += "<td>" + str(ticket["reporter"]) + "</td>\n"
			output += "<td>" + str(ticket["owner"]) + "</td>\n"
			output += "<td width="">" + coment_id_list + "</td>\n"
			output += "<td>" + str(comments_word_count) + "</td>\n"
			output += "</tr>\n"
			wikitext += "|| #" + ticket_id + " || " + '[#' + ticket_id + ' "' + ticket["name"] + '"] ||' + "\n" 
			
			# 计算该用户在这个帖子中所有回复的总字数。
			no_sort_warmhearted_reply[user] += comments_word_count
			
		output += "</table>"
		
		wikitext += "=== 统计信息 ===\n"
		wikitext += "|| 为自己开贴数 || 为別人开任务贴数 || 自行发回贴字数 || 热心回复字数 ||\n" 
		wikitext += "|| " + str(no_sort_ticket[user]) + " || " + str(no_sort_ticket_count_other[user]) + " || " + str(no_sort_reply_in_my_ticket[user]) + " || " + str(no_sort_warmhearted_reply[user]) + " ||\n" 
		
		output += "<h3>复制如下内容，替换自评贴中的“{Ticket内容列表}”</h3>\n"
		output += "<textarea cols=100 rows=10>" + wikitext + "</textarea>\n"
		output += "<div align=\"right\"><a href=\"#top\">返回顶部</a></div>\n"
		output += "<hr>\n"
	
	output += "</body></html>"

	# Sort all people in one month, the better the upper.
	sort_ticket = xxutils.asort( no_sort_ticket )
	sort_ticket_count_other = xxutils.asort( no_sort_ticket_count_other )
	sort_reply_in_my_ticket = xxutils.asort( no_sort_reply_in_my_ticket )
	sort_warmhearted_reply = xxutils.asort( no_sort_warmhearted_reply )
	
	config.REPLY_MY_TICKET[str(year+month)] = sort_reply_in_my_ticket
	config.REPLY_OTHER_TICKET[str(year+month)] = sort_warmhearted_reply

	current = year + month + ".html"
	index += "<table width=100% border=0><tr><td><table  border=1>\n"
	index += "<tr><th>姓名</th><th>为自己开贴数</th></tr>\n"
	for user, words in sort_ticket :
		index += "<tr><td><a href='" + current + "#" + user + "-create4myself'> " + user + "</a> </td><td> " + str(words) + "</tr>\n"
	
	index += "</table></td><td>\n<table  border=1>\n"
	index += "<tr><th>姓名</th><th>为别人开任务贴数</th></tr>\n"
	for user, words in sort_ticket_count_other :
		index += "<tr><td><a href='" + current + "#" + user + "-create4others'> " + user + "</a> </td><td> " + str(words) + "</tr>\n"
			
	index += "</table></td><td>\n<table  border=1>"
	index += "<tr><th>姓名</th><th>自行发贴字数</th></tr>\n"
	for user, words in sort_reply_in_my_ticket :
		index += "<tr><td><a href='" + current + "#" + user + "'> " + user + "</a> </td><td> " + str(words) + "</tr>\n"
			
	index += "</table></td><td>\n<table  border=1>\n"
	index += "<tr><th>姓名</th><th>热心回复字数</th></tr>\n"
	for user, words in sort_warmhearted_reply :
		index += "<tr><td><a href='" + current + "#" + user + "'> " + user + "</a> </td><td> " + str(words) + "</tr>\n"
	
	index += "</table></td></tr></table>"
	
  	pathname = config.TRAC_OUTPUT_PATH + "/ticket" + "/" + year + month + ".html"
	f = open(pathname, 'w')
	f.write(header + index + output)
	f.close()
	
	return index

def TicketDealAllMonth(conn, month_list):
	
	# First page of ticket statistics.
	index_filepath = config.TRAC_OUTPUT_PATH + "/ticket" + "/index.html"
	index = '''
	<html>\n
		<head>\n
			<title>Ticket统计 -- Superpolo Platform团队</title>\n
			<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />\n
		</head>\n
		<body>\n
			<h1>Ticket统计</h1>\n
	'''
	index += "<i>Generated: " + str(datetime.now()) + "</i>"
	
	# Every month
	for year, month in month_list:
		index += "\t\t<h2><a target=\"_blank\" href='" + year + month + ".html'>" + year + "年" + month + "月 </a></h2> \n"
		index += TicketDealOneMonth(conn, year, month)
	
	f = open(index_filepath, 'w')
	f.write(index)
	f.close()
