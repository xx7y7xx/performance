#!/bin/bash

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

IP="192.168.1.153"
ULIST="userlist.txt"
DATE="`date +'%Y年%m月份'`"

# 192.168.2.21
XXUTILS="/tmp/xxutils.sh"

# load useful functions
wget -q https://raw.githubusercontent.com/sp-chenyang/xxutils/master/xxutils.sh?$RANDOM -O $XXUTILS \
    && chmod a+x $XXUTILS \
    && . $XXUTILS

# just debug
#cat $XXUTILS

#
# send mail notification
#

SUBJECT="${DATE}绩效统计"
MSG="请将自己的绩效统计表格扔到\n\\\\192.168.2.21\\share\\Review\\`date +'%Y-%m'`"

xsendmail "$SUBJECT" "$MSG" "glue@spolo.org,wanghongliang@spolo.org"
