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

from parse import parse_odt

#reload(sys)
#sys.setdefaultencoding('utf8') 

class parse_Tests(unittest.TestCase):
    def test1(self):
        expect = [11200, 3000, 698, 60, 50, 40, 30, 20]
        nl = parse_odt("testdata/test1.odt")
        log = "\nExpect : %s\nBut return %s" % (expect, nl)
        self.assertTrue(nl == expect, msg = log)

    def test2(self):
        expect = [4313, 422, 0, 0, 16174, 2, 0, 0]
        nl = parse_odt("testdata/test2.odt")
        log = "\nExpect : %s\nBut return %s" % (expect, nl)
        #self.assertTrue(nl == expect, msg = log)

def main():
    unittest.main()

if __name__ == '__main__':
    main()

# end
