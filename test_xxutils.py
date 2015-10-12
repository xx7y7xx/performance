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

from xxutils import get_user_list_from_trac

#reload(sys)
#sys.setdefaultencoding('utf8')

class get_user_list_from_trac_Tests(unittest.TestCase):
    def test1(self):
        """Test get_user_list_from_trac function
        must include people
        """
        expect = "chenzhongming"
        ul = get_user_list_from_trac()
        log = "\nExpect : %s in user list array.\nBut list is %s" % (expect, ul)
        self.assertTrue(expect in ul, msg = log)

    def test2(self):
        """Test get_user_list_from_trac function
        must not include people
        """
        not_expect = "chenyang"
        ul = get_user_list_from_trac()
        log = "\nExpect : %s not in user list array.\nBut list is %s" % (not_expect, ul)
        self.assertTrue(not_expect not in ul, msg = log)

def main():
    unittest.main()

if __name__ == '__main__':
    main()

# end
