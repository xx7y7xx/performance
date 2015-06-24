#!/bin/bash

# CI Env

#WORKSPACE="/superpolo/data/statsvn"

DATADIR="/superpolo/data"
SVNDIR="${WORKSPACE}/svn_checkout"
STATSVN="/superpolo/bin/statsvn.jar"
STATSVN_COMMON_ARG="-verbose -charset utf-8 -disable-twitter-button -username ci -password sp12345678"
WWW_DEST="/public/www/statistics/svn"
SSTMP="/tmp/statsvn_6CLVpVKLe4nNDunN" # statsvn tmp dir
SVNPARAM=" --username=ci --password=sp12345678 --no-auth-cache "

# one repo at a time
## $1 modual name
stat_repo()
{
	local sr_modulename="$1"
	
	echo "Processing [${sr_modulename}] ... "
	
	local sr_svn_dir="${SVNDIR}/${sr_modulename}"
	
	local sr_svn_log="${SVNDIR}/${sr_modulename}.log"
	local sr_statsvn_log="${SVNDIR}/${sr_modulename}.statsvn.log"
	local sr_cache_dir="${SVNDIR}/${sr_modulename}_cache"
	local sr_output_dir="${SSTMP}/html/${sr_modulename}"
	
	# create svn log, xml format
	svn log $SVNPARAM -v --xml ${sr_svn_dir} > ${sr_svn_log}
    echo "status code of svn log is : [$?]"
	mkdir -p ${sr_output_dir}
	
	# prepare arguments, and call statsvn.
	local sr_statsvn_arg="${sr_svn_log} ${sr_svn_dir} -cache-dir ${sr_cache_dir} -output-dir ${sr_output_dir} -title ${sr_modulename} ${STATSVN_COMMON_ARG}"
	java -jar ${STATSVN} ${sr_statsvn_arg} &> ${sr_statsvn_log}
    echo "status code of statscn.jar : [$?]"
}

# Docbook stat
## $1 modual name
stat_docbook()
{
	local sr_modulename="$1"
	
	echo "Processing [${sr_modulename}] ... "
	
	local sr_svn_log="${SVNDIR}/${sr_modulename}_docbook.log"
	local sr_svn_dir="${SVNDIR}/${sr_modulename}/trunk/doc"
	local sd_cache_dir="${SVNDIR}/${sr_modulename}_cache"
	local sr_output_dir="${WWW_DEST}/nofilter/doc"

	svn log $SVNPARAM -v --xml ${sr_svn_dir} > ${sr_svn_log}
	
	mkdir -p ${sr_output_dir}
	
	local sr_statsvn_arg="${sr_svn_log} ${sr_svn_dir} -cache-dir ${sd_cache_dir} -output-dir ${sr_output_dir} -title ${sr_modulename} ${STATSVN_COMMON_ARG}"
	
	sudo java -jar ${STATSVN} ${sr_statsvn_arg}
}

#
# main()
#

# start time
date

cd ${WORKSPACE}

#####################################################################

# begin to stat

rm -rf $SSTMP
mkdir -p $SSTMP

date

#stat_repo "spp"
#stat_repo "ci"
#stat_repo "webtools"
#stat_repo "tooltpl"
#stat_repo "cff"
stat_repo "glue"
#stat_repo "spp_sdk_1010m"
#stat_repo "app_project"

# stat for docbook
#stat_docbook "ci"

date

# remove last result data.
rm -rf $WWW_DEST/*

# statsvn generated html.
cp -r $SSTMP/html/* ${WWW_DEST}

# first page of stat website.
cp "$SVNDIR/glue/trunk/stat/stat.html" ${WWW_DEST}/../stat.html

# first page of statsvn website.
cp "$SVNDIR/glue/trunk/stat/statsvn/index.html" ${WWW_DEST}

# Glue SVN Stat Page. (auto remove "sp:autocreated")
cp "$SVNDIR/glue/trunk/stat/statsvn/stat.html" ${WWW_DEST}
cp "$SVNDIR/glue/trunk/stat/statsvn/stat.js" ${WWW_DEST}

sudo chown www-data:www-data ${WWW_DEST} -R
sudo chmod g+w ${WWW_DEST} -R

# end time
date

# end
