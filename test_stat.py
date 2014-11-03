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

from spolo.stat import get_file_list
from spolo.stat import get_user_list

#reload(sys)
#sys.setdefaultencoding('utf8') 

class parse_Tests(unittest.TestCase):
    def test1(self):
        expect = [
            '/home/chenyang/source/performance/testdata/test1.odt',
            '/home/chenyang/source/performance/testdata/test2.odt',
        ]
        filelist = get_file_list()
        print filelist
        #log = "\nExpect : %s\nBut return : %s" % (expect, filelist)
        #self.assertTrue(nl == expect, msg = log)

class get_user_list_Tests(unittest.TestCase):
    def test1(self):
        not_expect = []
        userlist = get_user_list()
        log = "\nNot Expect : %s\nBut return : %s" % (not_expect, userlist)
        self.assertFalse(userlist == not_expect, msg = log)
    def test2(self):
        not_expect = "masol"
        userlist = get_user_list()
        log = "\nNot Expect : %s\nBut return : %s" % (not_expect, userlist)
        self.assertFalse((not_expect in userlist), msg = log)



def main():
    unittest.main()

if __name__ == '__main__':
    main()

# end
