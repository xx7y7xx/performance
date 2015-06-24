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
# There are no contributions in wiki changing ( or your format is wrong ) .
#

# wiki format is wrong( w/o "{{{" ? )
class NoCode_Tests(unittest.TestCase):
    # wiki page has only one revision.
    def test1(self):
        self.assertTrue(xxutils.wikicc("") == 0)
        self.assertTrue(xxutils.wikicc(" ") == 0)
        self.assertTrue(xxutils.wikicc("\t") == 0)
        self.assertTrue(xxutils.wikicc("abc") == 0)
        self.assertTrue(xxutils.wikicc("a b c") == 0)
        self.assertTrue(xxutils.wikicc("abc\ndef") == 0)
        self.assertTrue(xxutils.wikicc("{{{abc") == 0)
        self.assertTrue(xxutils.wikicc("abc{{{def") == 0)
        self.assertTrue(xxutils.wikicc("abc}}}def") == 0)
        self.assertTrue(xxutils.wikicc("abc}}}") == 0)
    # wiki page has more than one revision.
    def test2(self):
        self.assertTrue(xxutils.wikicc("{{{abc}}}", "") == 0)
        self.assertTrue(xxutils.wikicc("{{{abc}}}", "abc") == 0)
        self.assertTrue(xxutils.wikicc("{{{abc}}}", "def") == 0)
        self.assertTrue(xxutils.wikicc("abc", "def") == 0)
        self.assertTrue(xxutils.wikicc("abc", "abc") == 0)
        self.assertTrue(xxutils.wikicc("abc", "") == 0)

# No contribution in wiki changing.
class NoContribution_Tests(unittest.TestCase):
    def test1(self):
        self.assertTrue(xxutils.wikicc("{{{abc}}}", "{{{ a b c }}}") == 0)
        self.assertTrue(xxutils.wikicc("{{{abc}}}", "{{{\ta\tb\tc\t}}}") == 0)

#
# There are contributions in wiki changing.
#

class SingleLine_Tests(unittest.TestCase):
    def test1(self):
        self.assertTrue(xxutils.wikicc("{{{abc}}}") == 3)
    def test4(self):
        self.assertTrue(xxutils.wikicc("{{{ a b c }}}") == 3)

class MultiLines_Tests(unittest.TestCase):

    def test2(self):
        text = """{{{
abc
def
ghi
}}}"""
        c = xxutils.wikicc(text)
        #print c
        self.assertTrue(c == 9)
    def test3(self):
        text1 = """{{{
aaa
bbb
ccc
ddd
eee
}}}"""
        text2 = """{{{
aa
ccc
dddd
}}}"""
        c = xxutils.wikicc(text1, text2)
        #print c
        self.assertTrue(c == 6)
    def test5(self):
        text1 = """abc
def
ghi"""
        text2 = """def
ghi
jkl"""
        self.assertTrue(xxutils.wikicc(text1, text2) == 0)
    def test6(self):
        text1 = """{{{
abc
def
ghi
}}}"""
        text2 = """def
ghi
jkl"""
        self.assertTrue(xxutils.wikicc(text1, text2) == 0)
    def test7(self):
        text1 = """abc
def
ghi"""
        text2 = """{{{
def
ghi
jkl
}}}"""
        self.assertTrue(xxutils.wikicc(text1, text2) == 9)

def main():
    unittest.main()

if __name__ == '__main__':
    main()

# end
