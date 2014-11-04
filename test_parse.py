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


import os

import unittest
import datetime

from parse import parse_odt
from parse import get_uname_list
from parse import create_ods

#reload(sys)
#sys.setdefaultencoding('utf8')

TESTDIR = "/home/chenyang/source/performance/testdata"

class parse_Tests(unittest.TestCase):
    def test1(self):
        expect = [11200, 3000, 698, 60, 50, 40, 30, 20]
        nl = parse_odt(TESTDIR+"/test1.odt")
        log = "\nExpect : %s\nBut return %s" % (expect, nl)
        self.assertTrue(nl == expect, msg = log)

    def test2(self):
        expect = [4313, 422, 0, 0, 16174, 2, 0, 0]
        nl = parse_odt(TESTDIR+"/test2.odt")
        log = "\nExpect : %s\nBut return %s" % (expect, nl)
        #self.assertTrue(nl == expect, msg = log)

class get_uname_list_Tests(unittest.TestCase):
    def test1(self):
        """Test get_uname_list function
        must include people
        """
        expect = "chenzhongming"
        ul = get_uname_list()
        log = "\nExpect : %s in user list array.\nBut list is %s" % (expect, ul)
        self.assertTrue(expect in ul, msg = log)

    def test2(self):
        """Test get_uname_list function
        must not include people
        """
        not_expect = "chenyang"
        ul = get_uname_list()
        log = "\nExpect : %s not in user list array.\nBut list is %s" % (not_expect, ul)
        self.assertTrue(not_expect not in ul, msg = log)

class create_ods_Tests(unittest.TestCase):
    def test1(self):
        """Test create_ods function
        must create a ods file
        """
        expect = TESTDIR+"/create_ods.ods"
        create_ods(expect)
        log = "\nExpect : %s file created.\nBut file not exist" % (expect)
        self.assertTrue(os.path.isfile(expect), msg = log)
        print "Try to remove test file..."
        os.remove(expect)

def main():
    unittest.main()

if __name__ == '__main__':
    main()

# end
