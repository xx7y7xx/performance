#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

#/**************************************************************************
# *
# *  This file is part of the OSC(Open Source Communit).
# *  Copyright (C) by SanPolo Co.Ltd.
# *  All rights reserved.
# *
# *  See http://osc.spolo.org/ for more information.
# *
# *  SanPolo Co.Ltd
# *  http://www.spolo.org/  spolo@spolo.org sales@spolo.org
# *
#**************************************************************************/

import sys

#import argparse  # new in python2.7
import optparse   # old python

from sqlite3 import dbapi2 as sqlite2

import config
import xxutils

import ticket
import wiki
import code
import table

reload(sys)
sys.setdefaultencoding('utf8')

# 参数定义

# new in python 2.7
#parser = argparse.ArgumentParser(description = "stattrac")
#parser.add_argument('--db', action='store', dest='trac_db',
#                    help = "trac db path")
#parser.add_argument('--url', action='store', dest='trac_url',
#                    help = "trac url")
#parser.add_argument('--out', action='store', dest='trac_out',
#                    help = "trac output path")
#parser.add_argument('--debug', action='store', dest='stattrac_debug',
#                    help = "debug or not")
#args = parser.parse_args()

# old python
parser = optparse.OptionParser()
parser.add_option('--db', action='store', dest='trac_db',
                    help = "trac db path")
parser.add_option('--url', action='store', dest='trac_url',
                    help = "trac url")
parser.add_option('--out', action='store', dest='trac_out',
                    help = "trac output path")
parser.add_option('--debug', action='store', dest='stattrac_debug',
                    help = "debug or not")
args = parser.parse_args()


# 判断必须给定的参数

if args.trac_db is None :
    print "not given trac db."
    sys.exit()
if args.trac_url is None :
    print "not given trac url."
    sys.exit()
if args.trac_out is None :
    print "not given trac output path."
    sys.exit()

config.TRAC_DB_PATH = args.trac_db
config.TRAC_URL = args.trac_url
config.TRAC_OUTPUT_PATH = args.trac_out
# 是否进行debug
if args.stattrac_debug is not None :
    config.DEBUG = True

xxutils.sp_debug("Trac db path : " + config.TRAC_DB_PATH)
xxutils.sp_debug("Trac url : " + config.TRAC_URL)
xxutils.sp_debug("Trac output path : " + config.TRAC_OUTPUT_PATH)

# global var
config.TRAC_WIKI_URL = config.TRAC_URL + "/wiki"
config.TRAC_TICKET_URL = config.TRAC_URL + "/ticket"

# main()

conn = sqlite2.connect(config.TRAC_DB_PATH)

all_month = conn.cursor()
all_month.execute('''
SELECT
    distinct strftime('%Y', time/1000000, 'unixepoch', 'localtime') as year,
    strftime('%m', time/1000000, 'unixepoch', 'localtime') as month
FROM
    ticket
ORDER BY
    strftime('%Y', time/1000000, 'unixepoch', 'localtime') desc,
    strftime('%m', time/1000000, 'unixepoch', 'localtime') desc
''')

# Every month
all_month_list = []
for year, month in all_month:
    all_month_list.append( (year, month) )

all_month.close()

wiki.WikiDealAllMonth(conn)
code.WikiDealAllMonth(conn)
ticket.TicketDealAllMonth(conn, all_month_list)

table.TicketAndWikiWords(conn)

# EOF
