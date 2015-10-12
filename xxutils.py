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

def get_name(fn) :
    return fn.replace(".odt", "").strip()

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

def get_user_list_from_trac() :
    """Get user list from glue trac."""
    try:
        username = "ci"
        password = "sp12345678"
        top_level_url = "http://glue.spolo.org"
        url = "http://glue.spolo.org/trac/glue/wiki/%E5%BC%80%E5%8F%91%E4%BA%BA%E5%91%98%E4%BF%A1%E6%81%AF?format=txt"

        # create a password manager
        password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        
        # Add the username and password.
        # If we knew the realm, we could use it instead of None.
        password_mgr.add_password(None, top_level_url, username, password)
        
        handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        
        # create "opener" (OpenerDirector instance)
        opener = urllib2.build_opener(handler)
        
        # use the opener to fetch a URL
        response = opener.open(url)

    except HTTPError as e:
        msg = "URL : %s\n" % url
        msg += 'Server return code : %s' % e.code
        print(msg)
    #except e:
    #    print(('Unexpected exception thrown:', e))

    raw_data = response.read().decode('utf-8')
    #print raw_data

    # get real developer
    ret = []
    for line in raw_data.splitlines():
        # find all developer from email address.
        m = re.search(r"(\w+)@spolo.org", line)
        if m:
            name = m.group(1)

            # not developer.
            if name in ["liwei", "hanlu", "changyushan", "peizhelun", "tangying"]:
                continue

            ret.append(name)

    return ret

# end
