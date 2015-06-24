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
import logging
import sys

import wiki

#reload(sys)
#sys.setdefaultencoding('utf8') 

#
# There are no contributions in wiki changing ( or your format is wrong ) .
#

class SingleLine_Tests(unittest.TestCase):
    def test1(self):
        log= logging.getLogger( "SomeTest.testSomething" )
        #log.debug( "this= %r", self.this )
        #log.debug( "that= %r", self.that )
        self.assertTrue(wiki.wikiwc("apple bug") == 2)
    def test2(self):
        self.assertTrue(wiki.wikiwc("applebug") == 1)
    def test3(self):
        wc = wiki.wikiwc("bug", "apple")
        expect = 1
        self.assertTrue(wc == expect, msg='result:[{0}], expect:[{1}]'.format(wc, expect))
    def test4(self):
        wc = wiki.wikiwc("apple", "bug")
        expect = 1
        self.assertTrue(wc == expect, msg='result:[{0}], expect:[{1}]'.format(wc, expect))
    def test5(self):
        rev1 = "apple bug"
        rev2 = "bug apple"
        wc = wiki.wikiwc(rev1, rev2)
        expect = 2
        self.assertTrue(wc == expect, msg='\nrev1:[{0}]\nrev2:[{1}]\nresult:[{2}], expect:[{3}]'.format(rev1, rev2, wc, expect))

class MultiLines_Tests(unittest.TestCase):

    def test1(self):
        text = """abc
def
ghi"""
        wc = wiki.wikiwc(text)
        #print c
        self.assertTrue(wc == 3)
    def test2(self):
        rev1 = """aaa
bbb
ccc
ddd
eee"""
        rev2 = """aa
ccc
dddd"""
        wc = wiki.wikiwc(rev1, rev2)
        expect = 2
        self.assertTrue(wc == expect, msg='\nrev1:[{0}]\nrev2:[{1}]\nresult:[{2}], expect:[{3}]'.format(rev1, rev2, wc, expect))
    def test3(self):
        rev1 = """{{{
aaa
bbb
ccc
ddd
eee
}}}"""
        rev2 = """aa
ccc
dddd"""
        wc = wiki.wikiwc(rev1, rev2)
        expect = 3
        self.assertTrue(wc == expect, msg='\nrev1:[{0}]\nrev2:[{1}]\nresult:[{2}], expect:[{3}]'.format(rev1, rev2, wc, expect))

def main():
    logging.basicConfig( stream=sys.stderr )
    logging.getLogger( "SomeTest.testSomething" ).setLevel( logging.DEBUG )
    unittest.main()

if __name__ == '__main__':
    main()

# end
