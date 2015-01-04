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
import datetime

import xxutils

#reload(sys)
#sys.setdefaultencoding('utf8') 

class getDate_Tests(unittest.TestCase):
    def test1(self):
        expect = datetime.datetime(2014, 8, 1)
        
        for day in range(16, 32):
            fakenow = datetime.datetime(2014, 8, day)
            date = xxutils.getDate(fakenow)
            self.assertTrue(date == expect)
        
        for day in range(1, 16):
            fakenow = datetime.datetime(2014, 9, day)
            date = xxutils.getDate(fakenow)
            self.assertTrue(date == expect)

    def test2(self):
        expect = datetime.datetime(2014, 12, 1)
        fakenow = datetime.datetime(2015, 1, 4)
        date = xxutils.getDate(fakenow)
        self.assertTrue(date == expect)

def main():
    unittest.main()

if __name__ == '__main__':
    main()

# end
