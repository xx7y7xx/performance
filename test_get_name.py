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
        expect = "liuzhishuang"
        filename = "liuzhishuang .odt"
        username = xxutils.get_name(filename)
        self.assertTrue(username == expect)

def main():
    unittest.main()

if __name__ == '__main__':
    main()

# end
