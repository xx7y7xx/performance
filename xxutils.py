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
    if now.day > 15 :
        ret = datetime.datetime(now.year, now.month, 1)
    else:
        ret = datetime.datetime(now.year, (now.month -1), 1)
    return ret

# end
