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

# create random dir for me
JDIR="/tmp/jixiao_$RANDOM$RANDOM$RANDOM$RANDOM$RANDOM$RANDOM"
mkdir -p "$JDIR"
cd "$JDIR"

# load useful functions
wget -q https://raw.githubusercontent.com/sp-chenyang/xxutils/master/xxutils.sh \
    && chmod a+x xxutils.sh \
    && . xxutils.sh

# Get user list from trac
# gen userlist.txt
getusers

# create ticket for each user.
while read -r username;
do
    cmd='sudo python /home/chenyang/tool/newticket.py'
    cmd="$cmd --reporter ci"
    cmd="$cmd --owner \"$username\""
    cmd="$cmd --type review"
    cmd="$cmd --summary \"${DATE}绩效统计 - 每月自评表\""
    cmd="$cmd --description \"提交本月自评表\""
    echo $cmd
    rcmd "$IP" "$cmd"
done < $ULIST

#
# send mail notification
#

SUBJECT="${DATE}绩效统计"
MSG="请将自己的绩效统计表格扔到\nsmb://192.168.2.21/share/Review/`date +'%Y-%m'`"

xsendmail "$SUBJECT" "$MSG" "glue@spolo.org"
