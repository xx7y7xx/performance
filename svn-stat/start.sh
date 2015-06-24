#!/bin/bash

# Run this as a jenkins job

# CI Env

#WORKSPACE="/var/lib/jenkins/jobs/svn-stat/workspace"

SVNDIR="${WORKSPACE}/tmp/svn"
STATSVN="${WORKSPACE}/opt/statsvn-0.7.0/statsvn.jar"
OUTPUT="${WORKSPACE}/output"
STATSVN_ARG="-verbose -charset utf-8 -disable-twitter-button -username ci -password sp12345678"
SVNPARAM=" --username=ci --password=sp12345678 --no-auth-cache "

# one repo at a time
## $1 modual name
stat_repo()
{
	local sr_repo_name="$1"
	
	echo "Processing [${sr_repo_name}] ... "
	
	local sr_svn_dir="${SVNDIR}/${sr_repo_name}"
	local sr_svn_log="${SVNDIR}/${sr_repo_name}.log"
	local sr_statsvn_log="${SVNDIR}/${sr_repo_name}.statsvn.log"
	local sr_cache_dir="${SVNDIR}/${sr_repo_name}_cache"
	local sr_output_dir="${OUTPUT}/${sr_repo_name}"
	
  # Do a fresh checkout or update exist one.
  if [ -d $sr_svn_dir ]; then
    svn update $SVNPARAM $sr_svn_dir
  else
    svn checkout $SVNPARAM http://glue.spolo.org/svn/$sr_repo_name $sr_svn_dir
  fi

	# create svn log, xml format
	svn log $SVNPARAM -v --xml ${sr_svn_dir} > ${sr_svn_log}
    echo "status code of svn log is : [$?]"
	mkdir -p ${sr_output_dir}
	
	# prepare arguments, and call statsvn.
	local sr_statsvn_arg="${sr_svn_log} ${sr_svn_dir} -cache-dir ${sr_cache_dir} -output-dir ${sr_output_dir} -title ${sr_repo_name} ${STATSVN_ARG}"
	java -jar ${STATSVN} ${sr_statsvn_arg} &> ${sr_statsvn_log}
    echo "status code of statscn.jar : [$?]"
}

#
# main()
#

# start time
date

cd ${WORKSPACE}

#####################################################################

# begin to stat

# clear last result data.
rm -rf $OUTPUT
mkdir -p $OUTPUT

date

#stat_repo "spp"
#stat_repo "ci"
#stat_repo "webtools"
#stat_repo "tooltpl"
#stat_repo "cff"
stat_repo "glue"
#stat_repo "spp_sdk_1010m"
#stat_repo "app_project"

date

# svn stat website
cp "$WORKSPACE"/svn-stat/www/* ${OUTPUT}

# end time
date

# end
