#!/bin/bash

# Run this as a jenkins job

# Jenkins env
#WORKSPACE="/var/lib/jenkins/jobs/svn-stat/workspace"

# Script env
SVNDIR="${WORKSPACE}/tmp/svn"
STATSVN="${WORKSPACE}/opt/statsvn-0.7.0/statsvn.jar"
OUTPUT="${WORKSPACE}/output"
STATSVN_ARG="-verbose -charset utf-8 -disable-twitter-button -username ci -password sp12345678"
SVNPARAM=" --username=ci --password=sp12345678 --no-auth-cache "

# Contains exclude cfg file for each repo.
ExcludeDirsCfgDir="${WORKSPACE}/svn-stat/exclude_dirs"

# one repo at a time
#   $1 - modual name
#   $2 - (Optional) path in this($1) modual.
#        When set, processing only the selected($2) path.
stat_repo() {
  local sr_repo_name="$1"
  local sr_repo_path="$2"
  
  echo "Processing [${sr_repo_name} : ${sr_repo_path}] ... "
  
  if [ -z $sr_repo_path ]; then
    local sr_svn_url="http://glue.spolo.org/svn/$sr_repo_name"
    local sr_repo_encode_name=$sr_repo_name
  else
    local sr_svn_url="http://glue.spolo.org/svn/$sr_repo_name/$sr_repo_path"
    # trunk/wware/tech.com -> trunk_wware_tech.com
    local sr_repo_encode_name="${sr_repo_name}_`echo $sr_repo_path | sed -e 's/\//_/g'`"
  fi

  local sr_svn_dir="${SVNDIR}/${sr_repo_encode_name}"
  local sr_svn_log="${SVNDIR}/${sr_repo_encode_name}.log"
  local sr_cache_dir="${SVNDIR}/${sr_repo_encode_name}_cache"
  local sr_output_dir="${OUTPUT}/${sr_repo_encode_name}"

  # Do a fresh checkout or update exist one.
  if [ -d $sr_svn_dir/.svn ]; then
    svn cleanup $sr_svn_dir
    svn update $SVNPARAM $sr_svn_dir
  else
    svn checkout $SVNPARAM $sr_svn_url $sr_svn_dir
  fi
  
  # create svn log, xml format
  svn log $SVNPARAM -v --xml ${sr_svn_dir} > ${sr_svn_log}
  local ret=$?
  if [ "X$ret" != "X0" ]; then
    echo "status code of svn log is [${ret}]."
    exit $ret
  fi
  mkdir -p ${sr_output_dir}
 
  # Exclude dir for statsvn
  exclude_dir=""
  for line in `cat ${ExcludeDirsCfgDir}/${sr_repo_encode_name}.txt`; do
    if [ ! -z $exclude_dir ]; then
      exclude_dir+=";"
    fi
    exclude_dir+="$line/**"
  done
  exclude_dir=" -exclude ${exclude_dir} "
  echo "[Debug] exclude dirs : " ${exclude_dir}
 
  # prepare arguments, and call statsvn.
  local sr_statsvn_arg="${sr_svn_log} ${sr_svn_dir} -cache-dir ${sr_cache_dir} -output-dir ${sr_output_dir} -title ${sr_repo_encode_name} ${exclude_dir} ${STATSVN_ARG}"
  java -jar ${STATSVN} ${sr_statsvn_arg}
  local ret=$?
  if [ "X$ret" != "X0" ]; then
    echo "status code of statsvn is [${ret}]."
    exit $ret
  fi
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
stat_repo "glue" "trunk/wware/wide.com"
stat_repo "glue" "trunk/wware/tech.com"
#stat_repo "spp_sdk_1010m"
#stat_repo "app_project"

date

# svn stat website
ls $WORKSPACE/svn-stat/www/*
cp $WORKSPACE/svn-stat/www/* ${OUTPUT}

# end time
date

# end
