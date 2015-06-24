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

class Common_Tests(unittest.TestCase):

    def test1(self):
        text = """Replying to [comment:12 chenyang]:
> abc
defg"""
        result = xxutils.sub_reply_content(text)
        # @TODO should fix the last \n in expect string
        expect = """defg
"""
        self.assertTrue(result == expect, msg='result:[{0}], expect:[{1}]'.format(result, expect))

    def test2(self):
        text = ""
        result = xxutils.sub_reply_content(text)
        # @TODO should fix the last \n in expect string
        expect = "\n"
        self.assertTrue(result == expect, msg='result:[{0}], expect:[{1}]'.format(result, expect))

    def test_none_type(self):
        text = None
        result = xxutils.sub_reply_content(text)
        expect = ""
        self.assertTrue(result == expect, msg='result:[{0}], expect:[{1}]'.format(result, expect))

def main():
    logging.basicConfig( stream=sys.stderr )
    logging.getLogger( "SomeTest.testSomething" ).setLevel( logging.DEBUG )
    unittest.main()

if __name__ == '__main__':
    main()

# end
