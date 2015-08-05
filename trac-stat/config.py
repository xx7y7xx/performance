#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

#/**************************************************************************
# *
# *  This file is part of the UGE(Uniform Game Engine).
# *  Copyright (C) by SanPolo Co.Ltd. 
# *  All rights reserved.
# *
# *  See http://uge.spolo.org/ for more information.
# *
# *  SanPolo Co.Ltd
# *  http://uge.spolo.org/  sales@spolo.org uge-support@spolo.org
# *
#**************************************************************************/

# 只列出在职人员，忽略一些用户，比如离职。
# 请按照字母顺序进行添加，这样方便查找。
SPP_USERS = (
    "chenyang",
    "chenzhongming",
    "cuiqiang",
    "dinghuihui",
    "fengmingming",
    "lilixiang",
    "liuliang",
    "liyingying",
    "lizhutang",
    "masol",
    "wanglingzhao",
    "wangxingzhuo",
    "wangyansheng",
    "xiejinrui",
    "xuxinlong",
    "yejunfu",
    "yutian",
    "zhanglinling",
    "zhaojinpeng"
)

# only default value, you can pass this value from 
# command line options per project.
TRAC_DB_PATH = "/spp/data/stattrac/trac.db"
TRAC_URL = "http://spp.spolo.org/trac/spp"
TRAC_OUTPUT_PATH = "/spp/data/stattrac"

# 是否进行调试
DEBUG = False

# 行结束符
EOL = "\r\n"
REPLY_MY_TICKET = {}
REPLY_OTHER_TICKET = {}
