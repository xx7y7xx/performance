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

import re
import datetime
import difflib

import config

# show debug info
def sp_debug(info) :
    print "[DEBUG] [" + timestamp() + "] " + info

# arsort() in PHP
# ref : http://webcache.googleusercontent.com/search?q=cache:GasqcGhxTxQJ:www.php2python.com/wiki/function.arsort/+&cd=1&hl=en&ct=clnk&gl=us&client=ubuntu
def asort(d):
    return sorted(d.items(), key=lambda x: x[1], reverse=True)

# 删除帖子回复中的reply部分，因为这部分数据是trac自动生成的，而不是开发人员的贡献。
# 比如：
# =============================================================================
# Replying to [comment:6 jigaihui]:
# > maxscript中通过getFacearea可以获得face的面积.
# > 对于需求的认识:
# 应该是第一个吧。我们的对照关系是基于总面积的。如果假定贴图的利用率是常数，这个对
# 照是异常精确的——贴图尺寸只应该和造型的总面积成比例关系。
# =============================================================================
# 经过处理之后剩下
# =============================================================================
# 应该是第一个吧。我们的对照关系是基于总面积的。如果假定贴图的利用率是常数，这个对
# 照是异常精确的——贴图尺寸只应该和造型的总面积成比例关系。
# =============================================================================
def sub_reply_content(oldstr) :
    if oldstr is None:
        print 'type['+str(type(oldstr))+']'
        print '['+str(oldstr)+']'
        return ''
    oldstr = oldstr.encode('utf8')
    assert isinstance(oldstr, str)
    newstr = ""
    lines = re.split("\n", oldstr) # xxdebug - try to fix http://192.168.2.21:8080/job/stattrac/1733/console
    for line in lines :
        if re.match("^> .*", line) is not None :
            continue
        if re.match("^Replying to \[comment:.*", line) is not None :
            continue
        newstr += line + "\n"
    return newstr

# 删除帖子/wiki中的代码块。
# 一般的，我们认为代码块都是从其他地方（源码中）copy过来的，所以不应该参与字数统计。
# 比如：
# =============================================================================
# 1
# 2
# {{{
# a
# b
# }}}
# 3
# 4 abc {{{ def }}} ghi
# 5
# {{{
# c
# d
# }}}
# 6
# =============================================================================
# 经过处理之后剩下  @ modify : yuxiangliang
# =============================================================================
# 1
# 2
# 3
# 4 abc  ghi    
# 5
# 6
# =============================================================================
def sub_code_block(code) :
    # 大括号及其中的内容全部删除
    pattern = r'\{{3}(.*?)\}{3}'
    pos = 0
    for match in re.finditer(pattern, code, re.DOTALL):
                s = match.start() - pos
                e = match.end() - pos
                code = code[:s] + code[e:]
                pos += e - s
            
    return code

# Compare 2 string, find the different line.
# Count the words of diff line from the first stirng.
def wiki_differ_wc(src1, src2) :
    # 去掉{{{...}}}中的内容。
    tmp = sub_code_block(src1)
    src1 = tmp
    tmp = sub_code_block(src2)
    src2 = tmp
    
    f1 = src1.split("\r\n")
    f2 = src2.split("\r\n")
    
    d1 = set(f1) - set(f2)
    
    s = '\r\n'.join(d1)
    return wc(s)

# 统计有效Unicode字数。
def cws(words):
    words = words.decode("utf8")
    count = 0
    for word in words.split("\\"):    #去掉可能的转义符号
        for e in re.compile("(\W)").split(word): # 分割
            reg = re.compile(r'\S', re.UNICODE) # 扔掉空格
            if  reg.match(e) :
                count = count + 1
    return count

# ticket中的字数统计，输入的内容可以是如下任意一种类型
# * summary
# * description
# * comment
def ticket_wc(s) : 
    # 删除reply部分的文字。
    tmp = sub_reply_content(s)
    # 删除代码块
    tmp2 = sub_code_block(tmp)
    
    return wc(tmp2)

# wiki中的字数统计。
# @fixme chenyang20120831 暂时不过滤“> ”包含的引用部分。
def wiki_wc(s) : 
    # 删除代码块
    tmp = sub_code_block(s)
    
    return wc(tmp)

# [word count] 统计有效字数。
def wc(words) :

    # chenyang20120831
    # wc函数应该保持单纯，只有字数统计功能，而没有过滤功能。
    ## 从需要计算字数的字符串中取出{{{...}}}包含的内容。
    ## 我们假定这部分内容全都是代码（code），进一步假定都是copy的内容。
    ## 需要计算这部分copy的内容的字数，然后从总字数中减掉。
    #codelist = re.findall("{{{.*?}}}", words, re.S)
    #code = ''.join(codelist)
    #code_count = cws(code)
    #
    ## 10个代码字符，只算作一个有效字数。
    ##return ( cws(words) - code_count + code_count/10 )
    ## 删除{{{...}}}中的字数
    #return ( cws(words) - code_count )
    return cws(words)

# [code count] 统计代码的字符数
# http://www.daniweb.com/software-development/python/code/216702/wordcount-similar-to-unix-wc-python
# number of all characters
def noc(text):
    return len(text)
# number of lines
def nol(text):
    # assumes lines end with '\n'
    # the last line usually has no '\n' so add 1 to count
    return code.count('\n') + 1
# number of words
def now(text):
    # assumes words are separated by whitespace
    wordlist = code.split(None)
    return len(wordlist)

# remove all empty char, ex: space, tab...
def xxstrip(text):
    # strip left-side and right-side space and tab
    tmp = text.strip()
    # remove space in string
    tmp = tmp.replace(" ", "")
    # strip line break
    return ''.join(tmp.splitlines())

# remove all empty char, ex: \t,\s
# not include line break(\n,\r)
def rm_whitespace(text):
    # strip left-side and right-side space and tab
    tmp = text.strip()
    # remove space(\s) in string
    tmp = tmp.replace(" ", "")
    # remove tab(\t) in string
    return tmp.replace("\t", "")

# remove line break, ex: \n, \r
def rm_linebreak(text):
    return ''.join(text.splitlines())

def find_first_code_block(text):
    if text.find("{{{") == -1:
        return False
    elif text.find("}}}") == -1:
        return False
    return text.split("{{{")[1].split("}}}")[0]

# diff new vs old code.
def find_diff_code_lines(old, new, split = "\r\n"):
    f1 = old.splitlines()
    f2 = new.splitlines()

    d = difflib.Differ()
    d1 = list(d.compare(f1, f2))

    new = []
    # code removed will not include.
    for line in d1:
        if line.startswith("+ ") != True:
            continue
        line = line.replace("+ ", "", 1)
        new.append(line)

    return split.join(new)

def createLink(link, name) :
    return "<a target=\"_blank\" href='" + link + "'>" + name + "</a>"

def createTicketLink(trac_url, ticket_id, name) :
    return createLink(trac_url + "/ticket/" + ticket_id, name)
def createCommentLink(trac_url, ticket_id, comment_id, name) :
    return createLink(trac_url + "/ticket/" + ticket_id + "#comment:" + comment_id, name)

def timestamp() :
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# source code in wiki
# in: wiki page name
def IsWikiSourcePage(pagename):
    pattern1 = r'\bsource'
    pattern2 = r'\bjiandan001/www'   
    return (re.match(pattern1, pagename, re.IGNORECASE) or re.match(pattern2, pagename, re.IGNORECASE))

# exclude some wiki
# in: wiki page name
def IsExcludeWiki(pagename):
    pattern1 = r'\bpersonal' # personal wiki
    pattern2 = r'\bexclude' # exclude wiki
    return (re.match(pattern1, pagename, re.IGNORECASE) or re.match(pattern2, pagename, re.IGNORECASE))

# count code in wiki text
# input must contains "{{{" & "}}}"
def wikicc(rev1, rev2 = None):
    # only one revision
    if rev2 == None :
        # remove "{{{" & "}}}", then diff.
        code = find_first_code_block(rev1)
        if code == False:
            return 0 # wiki has no code(or your format is wrong)
        
        code = rm_whitespace(code)
        code = rm_linebreak(code)
        return noc(code)
    # has previous revision.
    else :
        # remove "{{{" & "}}}", then diff.
        rev1_code = find_first_code_block(rev1)
        rev2_code = find_first_code_block(rev2)
        # a table shows that rev1 has code block, or rev2 has code block.
        #--------------------------------------------------------
        #          block    block    block     block
        #--------------------------------------------------------
        # rev1       v                 v
        # rev2       v        v            
        #--------------------------------------------------------
        # count    diff     rev2       0         0
        #--------------------------------------------------------
        if rev2_code == False:
            return 0
        if rev1_code == False:
            rev2_code = rm_whitespace(rev2_code)
            rev2_code = rm_linebreak(rev2_code)
            return noc(rev2_code)
        
        rev1_code = rm_whitespace(rev1)
        rev2_code = rm_whitespace(rev2)
        
        diff = find_diff_code_lines(rev1_code, rev2_code)

        diff = rm_linebreak(diff)
        return noc(diff)



#EOF
