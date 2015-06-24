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

import xxutils

#reload(sys)
#sys.setdefaultencoding('utf8') 

class SingleLine_Tests(unittest.TestCase):
    def test1(self):
        log= logging.getLogger( "SomeTest.testSomething" )
        #log.debug( "this= %r", self.this )
        #log.debug( "that= %r", self.that )
        self.assertTrue(xxutils.ticket_wc("apple bug") == 2)
    def test2(self):
        self.assertTrue(xxutils.ticket_wc("applebug") == 1)
    def test3(self):
        wc = xxutils.ticket_wc("bug {{{abc}}} apple")
        expect = 2
        self.assertTrue(wc == expect, msg='result:[{0}], expect:[{1}]'.format(wc, expect))
    def test_input_none(self):
        wc = xxutils.ticket_wc(None)
        expect = 0
        self.assertTrue(wc == expect, msg='result:[{0}], expect:[{1}]'.format(wc, expect))

class MultiLines_Tests(unittest.TestCase):

    def test1(self):
        text = """abc
{{{
def
}}}
ghi"""
        wc = xxutils.ticket_wc(text)
        self.assertTrue(wc == 2)
    def test2(self):
        text = """{{{
abc
def
ghi
}}}"""
        wc = xxutils.ticket_wc(text)
        self.assertTrue(wc == 0)
    def test3(self):
        text = """abc
{{{
ABC
{{{
XXX
}}}
DEF
}}}
def"""
        wc = xxutils.ticket_wc(text)
        expect = 2
        #@TODO should fix this bug.
        #self.assertTrue(wc == expect, msg='result:[{0}], expect:[{1}]'.format(wc, expect))

def main():
    logging.basicConfig( stream=sys.stderr )
    logging.getLogger( "SomeTest.testSomething" ).setLevel( logging.DEBUG )
    unittest.main()

if __name__ == '__main__':
    main()

# end
