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
        self.assertTrue(xxutils.sub_code_block("apple bug") == "apple bug")
    def test2(self):
        self.assertTrue(xxutils.sub_code_block("applebug") == "applebug")
    def test3(self):
        result = xxutils.sub_code_block("bug {{{abc}}} apple")
        expect = "bug  apple"
        self.assertTrue(result == expect, msg='result:[{0}], expect:[{1}]'.format(result, expect))

class MultiLines_Tests(unittest.TestCase):

    def test1(self):
        text = """abc
{{{
def
}}}
ghi"""
        result = xxutils.sub_code_block(text)
        expect = """abc

ghi"""
        self.assertTrue(result == expect, msg='result:[{0}], expect:[{1}]'.format(result, expect))
    def test2(self):
        text = """{{{
abc
def
ghi
}}}"""
        result = xxutils.sub_code_block(text)
        expect = ""
        self.assertTrue(result == expect, msg='result:[{0}], expect:[{1}]'.format(result, expect))
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
        result = xxutils.sub_code_block(text)
        expect = """abc
def"""
        #@TODO should fix this bug.
        #self.assertTrue(result == expect, msg='result:[{0}], expect:[{1}]'.format(result, expect))

def main():
    logging.basicConfig( stream=sys.stderr )
    logging.getLogger( "SomeTest.testSomething" ).setLevel( logging.DEBUG )
    unittest.main()

if __name__ == '__main__':
    main()

# end
