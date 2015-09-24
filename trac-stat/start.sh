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

STATTRAC="$WORKSPACE/trac-stat/stattrac.py"
TMP="$WORKSPACE/trac-stat/tmp"
OUTPUT="$WORKSPACE/trac-stat/output"
PROJ="glue"

HOST="${PROJ}.spolo.org"

echo "Trac Statistics - ${HOST}"

# Clean

echo "Remove old sqlite db..."
rm -fv $TMP/${PROJ}

# init

echo "Making new dir..."
mkdir -p $TMP/${PROJ}
mkdir -p $OUTPUT/${PROJ}/ticket
mkdir -p $OUTPUT/${PROJ}/wiki
mkdir -p $OUTPUT/${PROJ}/code
mkdir -p $OUTPUT/${PROJ}/table

# get db

echo "Get db file from trac server..."
ssh chenyang@${HOST} "cd /tmp ; cp /home/trac/${PROJ}/db/trac.db ./trac.db ; tar zcvf trac.db.tar.gz trac.db"
scp -P 22 chenyang@${HOST}:/tmp/trac.db.tar.gz $TMP/${PROJ}
tar zxvf $TMP/${PROJ}/trac.db.tar.gz -C $TMP/${PROJ}

# begin

echo "Begin to parse db file..."
python $STATTRAC --url="http://${PROJ}.spolo.org/trac/${PROJ}" --db="${TMP}/${PROJ}/trac.db" --out="${OUTPUT}/${PROJ}" #--debug=chenyang
if [ $? -ne 0 ]; then
        echo "[ERROR] Python run error!"
        exit 1
fi

#EOF
