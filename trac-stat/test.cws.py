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

class CWS_Tests(unittest.TestCase):
    def test1(self):
        self.assertTrue(xxutils.cws("") == 0)
    def test2(self):
        self.assertTrue(xxutils.cws("1") == 1)
    def test3(self):
        self.assertTrue(xxutils.cws("bug") == 1)
    def test4(self):
        self.assertTrue(xxutils.cws("apple bug") == 2)
    def test5(self):
        self.assertTrue(xxutils.cws("sanpolo apple bug") == 3)
    def test6(self):
        wc = xxutils.cws("中文字符")
        expect = 4
        #print wc
        self.assertTrue(wc == expect)
    def test7(self):
        wc = xxutils.cws(" 中 文 字 符 ")
        expect = 4
        #print wc
        self.assertTrue(wc == expect)
    def test8(self):
        text = """aa
dddd"""
        expect = 2
        wc = xxutils.cws(text)
        self.assertTrue(wc == expect, msg='\ntext:[{0}]\nresult:[{1}], expect:[{2}]'.format(text, wc, expect))


def main():
    unittest.main()

if __name__ == '__main__':
    main()

# end
