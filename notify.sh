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
CMDFILE="rcmd.sh"
XXUTILS="/tmp/xxutils.sh"

# load useful functions
wget -q https://raw.githubusercontent.com/sp-chenyang/xxutils/master/xxutils.sh -o $XXUTILS \
    && chmod a+x $XXUTILS \
    && . $XXUTILS

# just debug
cat $XXUTILS

# create random dir for me
JDIR=$( gettmpdir "jixiao" )
cd "$JDIR"

# Get user list from trac
# gen userlist.txt
getusers
cat $ULIST

#
# create ticket for each user.
#

echo "" > $CMDFILE

while read -r username;
do
    cmd='sudo python /home/chenyang/tool/newticket.py'
    cmd="$cmd --reporter ci"
    cmd="$cmd --owner \"$username\""
    cmd="$cmd --type review"
    cmd="$cmd --summary \"${DATE}绩效统计 - 每月自评表\""
    cmd="$cmd --description \"提交本月自评表\""
    echo $cmd >> $CMDFILE
    # loop will break when using ssh
    # look at this : http://stackoverflow.com/a/1396070
    #rcmd "$IP" "$cmd"
done < $ULIST

# just for debug
cat $CMDFILE

rcmdfile "$IP" "$CMDFILE"

#
# send mail notification
#

SUBJECT="${DATE}绩效统计"
MSG="请将自己的绩效统计表格扔到\nsmb://192.168.2.21/share/Review/`date +'%Y-%m'`"

xsendmail "$SUBJECT" "$MSG" "glue@spolo.org"
