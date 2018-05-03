# Set of functions used in other scripts

config_general() {
	return 0
}

config_log_to_stdout() {
	return 0
}

runs_privileged() {
  test "$(id -u)" == "0"
  return $?
}

config_privileged() {
  # Change the s2i permissions back to the normal ones
  chmod 644 ${HTTPD_MAIN_CONF_PATH}/* && \
  chmod 755 ${HTTPD_MAIN_CONF_PATH} && \
  chmod 644 ${HTTPD_MAIN_CONF_D_PATH}/* && \
  chmod 755 ${HTTPD_MAIN_CONF_D_PATH} && \
  chmod 710 ${HTTPD_VAR_RUN}

  if ! [ -v HTTPD_LOG_TO_VOLUME ] ; then
    config_log_to_stdout
  fi
}

config_s2i() {
	return 0
}


config_non_privileged() {
  sed -i -e "s/^User apache/User default/" ${HTTPD_MAIN_CONF_PATH}/httpd.conf
  sed -i -e "s/^Group apache/Group root/" ${HTTPD_MAIN_CONF_PATH}/httpd.conf
  config_log_to_stdout
  if [ -v HTTPD_LOG_TO_VOLUME ] ; then
    echo "Error: Option HTTPD_LOG_TO_VOLUME is only valid for privileged runs (as UID 0)."
    return 1
  fi
}

# get_matched_files finds file for image extending
function get_matched_files() {
  local custom_dir default_dir
  custom_dir="$1"
  default_dir="$2"
  files_matched="$3"
  find "$default_dir" -maxdepth 1 -type f -name "$files_matched" -printf "%f\n"
  [ -d "$custom_dir" ] && find "$custom_dir" -maxdepth 1 -type f -name "$files_matched" -printf "%f\n"
}

# process_extending_files process extending files in $1 and $2 directories
# - source all *.sh files
#   (if there are files with same name source only file from $1)
function process_extending_files() {
  local custom_dir default_dir
  custom_dir=$1
  default_dir=$2
  while read filename ; do
    echo "=> sourcing $filename ..."
    # Custom file is prefered
    if [ -f $custom_dir/$filename ]; then
      source $custom_dir/$filename
    elif [ -f $default_dir/$filename ]; then 
      source $default_dir/$filename
    fi
  done <<<"$(get_matched_files "$custom_dir" "$default_dir" '*.sh' | sort -u)"
}

# Set current user in nss_wrapper
generate_container_user() {
  local passwd_output_dir="${HTTPD_APP_ROOT}/etc"

  export USER_ID=$(id -u)
  export GROUP_ID=$(id -g)
  envsubst < ${HTTPD_CONTAINER_SCRIPTS_PATH}/passwd.template > ${passwd_output_dir}/passwd
  export LD_PRELOAD=libnss_wrapper.so
  export NSS_WRAPPER_PASSWD=${passwd_output_dir}/passwd
  export NSS_WRAPPER_GROUP=/etc/group
}

# Copy config files from application to the location where httd expects them
# Param sets the directory where to look for files
process_config_files() {
  local dir=${1:-.}
  if [ -d ${dir}/httpd-cfg ]; then
    echo "---> Copying httpd configuration files..."
    if [ "$(ls -A ${dir}/httpd-cfg/*.conf)" ]; then
      cp -v ${dir}/httpd-cfg/*.conf "${HTTPD_CONFIGURATION_PATH}"
      rm -rf ${dir}/httpd-cfg
    fi
  else
    if [ -d ${dir}/cfg ]; then
      echo "---> Copying httpd configuration files from deprecated './cfg' directory, use './httpd-cfg' instead..."
      if [ "$(ls -A ${dir}/cfg/*.conf)" ]; then
        cp -v ${dir}/cfg/*.conf "${HTTPD_CONFIGURATION_PATH}"
        rm -rf ${dir}/cfg
      fi
    fi
  fi
}

# Copy SSL files provided in application source
process_ssl_certs() {
	return 0
}

