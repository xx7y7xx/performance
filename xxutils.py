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

import datetime

#reload(sys)
#sys.setdefaultencoding('utf8') 

def getDate(now = datetime.datetime.now()):
    """Get the stat month of this time."""
    now_day = now.day
    now_month = now.month
    now_year = now.year

    if now_day <= 15 :
        if now_month == 1:
            # last year
            now_month = 12
            now_year = now_year - 1
        else:
            now_month = now_month - 1
            assert now_month > 0

    return datetime.datetime(now_year, now_month, 1)

# end
