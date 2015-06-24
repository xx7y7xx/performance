#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

#/**************************************************************************
# *
# *  This file is part of the OSC(Open Source Community).
# *  Copyright (C) by SanPolo Co.Ltd. 
# *  All rights reserved.
# *
# *  See http://osc.spolo.org/ for more information.
# *
# *  SanPolo Co.Ltd
# *  http://www.spolo.org/  spolo@spolo.org sales@spolo.org
# *
#**************************************************************************/

import unittest

import xxutils

#reload(sys)
#sys.setdefaultencoding('utf8') 

#
# test
#

class wiki_differ_wc_Tests(unittest.TestCase):

    def test1(self):
        wc = xxutils.wiki_differ_wc("abc", "bcd")
        #print wc
        self.assertTrue(wc == 1)

class find_first_code_block_Tests(unittest.TestCase):

    def test1(self):
        code = xxutils.find_first_code_block("abc{{{def}}}ghi")
        #print code
        self.assertTrue(code == "def")
    def test2(self):
        code = xxutils.find_first_code_block("abc")
        self.assertTrue(code == False)

class noc_Tests(unittest.TestCase):

    def test1(self):
        count = xxutils.noc("abc")
        #print count
        self.assertTrue(count == 3)
    def test2(self):
        count = xxutils.noc(" a b c ")
        #print count
        self.assertTrue(count == 7)
    def test3(self):
        count = xxutils.noc("""abc
def
ghi""")
        #print count
        self.assertTrue(count == 11)

class xxstrip_Tests(unittest.TestCase):

    def test1(self):
        result = xxutils.xxstrip("abc")
        #print result
        self.assertTrue(result == "abc")
    def test2(self):
        result = xxutils.xxstrip(" a b c ")
        #print result
        self.assertTrue(result == "abc")
    def test3(self):
        result = xxutils.xxstrip("""abc
def
ghi""")
        #print result
        self.assertTrue(result == "abcdefghi")

class rm_whitespace_Tests(unittest.TestCase):

    def test1(self):
        result = xxutils.rm_whitespace("abc")
        #print result
        self.assertTrue(result == "abc")
    def test2(self):
        result = xxutils.rm_whitespace(" a b c ")
        #print result
        self.assertTrue(result == "abc")
    def test3(self):
        result = xxutils.rm_whitespace("\ta\tb\tc\t")
        #print result
        self.assertTrue(result == "abc")
    def test4(self):
        input = """ a b c 
\td\te\tf\t
  g  h  i  """
        expect = """abc
def
ghi"""
        result = xxutils.rm_whitespace(input)
        #print result
        self.assertTrue(result == expect)

class rm_linebreak_Tests(unittest.TestCase):

    def test1(self):
        result = xxutils.rm_linebreak("abc")
        #print result
        self.assertTrue(result == "abc")
    def test2(self):
        result = xxutils.rm_linebreak(" a b c ")
        #print result
        self.assertTrue(result == " a b c ")
    def test3(self):
        result = xxutils.rm_linebreak("\ta\tb\tc\t")
        #print result
        self.assertTrue(result == "\ta\tb\tc\t")
    def test4(self):
        input = """ a b c 
\td\te\tf\t
  g  h  i  """
        expect = """ a b c \td\te\tf\t  g  h  i  """
        result = xxutils.rm_linebreak(input)
        #print result
        self.assertTrue(result == expect)
    def test5(self):
        input = """ a b c \r\n\td\te\tf\t\r\n  g  h  i  \r\n"""
        expect = """ a b c \td\te\tf\t  g  h  i  """
        result = xxutils.rm_linebreak(input)
        #print result
        self.assertTrue(result == expect)

class find_diff_code_lines_Tests(unittest.TestCase):

    def test1(self):
        code1 = """aaa
bbb
ccc
ddd
eee"""
        code2 = """aa
ccc
dddd"""
        expect = """aa
dddd"""
        result = xxutils.find_diff_code_lines(code1, code2, "\n")
        #print "result : " + result
        #print "expect : " + expect
        self.assertTrue(result == expect)

class IsWikiSourcePage_Tests(unittest.TestCase):

    def test1(self):
        self.assertTrue(xxutils.IsWikiSourcePage("source/jiandan001/www/index.html"))
    def test2(self):
        self.assertTrue(xxutils.IsWikiSourcePage("jiandan001/www/index.html"))
    def test3(self):
        self.assertTrue(xxutils.IsWikiSourcePage("source/xuanran001/www/user-center/changshang/furniture.html"))

class IsExcludeWiki_Tests(unittest.TestCase):

    def test1(self):
        self.assertTrue(xxutils.IsExcludeWiki("personal"))
    def test2(self):
        self.assertTrue(xxutils.IsExcludeWiki("personal/chenyang"))
    def test3(self):
        self.assertTrue(xxutils.IsExcludeWiki("exclude"))
    def test4(self):
        self.assertTrue(xxutils.IsExcludeWiki("exclude/chenyang"))

def main():
    unittest.main()

if __name__ == '__main__':
    main()

# end
