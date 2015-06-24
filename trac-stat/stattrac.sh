#!/bin/bash

# arg[0] stattrac.py路径
#        eg. "/spp/data/stattrac/svn/stattrac.py"
# arg[1] 临时文件夹
#        eg. "/spp/data/stattrac"
# arg[2] www根目录
#        eg. "/public/www"
# arg[2] 项目名称
#        eg. "spp" 或者 "glue"

# == output ==
# status code
# 0 success
# 1 python run error

STATTRAC=$1
STATTRACTMP=$2
WWWROOT=$3
PROJ=$4

HOST="${PROJ}.spolo.org"

echo "Trac Statistics - ${HOST}"

# Clean

echo "Remove old sqlite db..."
rm -fv $STATTRACTMP/${PROJ}/trac.db.tar.gz
rm -fv $STATTRACTMP/${PROJ}/trac.db

# init

echo "Making new dir..."
mkdir -p $STATTRACTMP/${PROJ}/ticket
mkdir -p $STATTRACTMP/${PROJ}/wiki
mkdir -p $STATTRACTMP/${PROJ}/code
mkdir -p $STATTRACTMP/${PROJ}/table
mkdir -p $WWWROOT/statistics/${PROJ}_trac/ticket
mkdir -p $WWWROOT/statistics/${PROJ}_trac/wiki
mkdir -p $WWWROOT/statistics/${PROJ}_trac/code
mkdir -p $WWWROOT/statistics/${PROJ}_trac/table

# get db

echo "Get db file from trac server..."
ssh chenyang@${HOST} "cd /tmp ; cp /home/trac/${PROJ}/db/trac.db ./trac.db ; tar zcvf trac.db.tar.gz trac.db"
scp -P 22 chenyang@${HOST}:/tmp/trac.db.tar.gz $STATTRACTMP/${PROJ}
tar zxvf $STATTRACTMP/${PROJ}/trac.db.tar.gz -C $STATTRACTMP/${PROJ}

# begin

echo "Begin to parse db file..."
python $STATTRAC --url="http://${PROJ}.spolo.org/trac/${PROJ}" --db="${STATTRACTMP}/${PROJ}/trac.db" --out="${STATTRACTMP}/${PROJ}" #--debug=chenyang
if [ $? -ne 0 ]; then
	echo "[ERROR] Python run error!"
	exit 1
fi

# move to www root

echo "Moving statistics html file to apache root dir..."
mv $STATTRACTMP/${PROJ}/ticket/* $WWWROOT/statistics/${PROJ}_trac/ticket/
mv $STATTRACTMP/${PROJ}/wiki/* $WWWROOT/statistics/${PROJ}_trac/wiki/
mv $STATTRACTMP/${PROJ}/code/* $WWWROOT/statistics/${PROJ}_trac/code/
mv $STATTRACTMP/${PROJ}/table/* $WWWROOT/statistics/${PROJ}_trac/table/

#EOF
