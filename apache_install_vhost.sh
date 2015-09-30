#!/bin/bash
SCRIPT_NAME="$(basename ${0})"
############################################################################### 
# HEADER BEGIN
############################################################################### 
# USAGE
#   /path/to/${SCRIPT_NAME} [-hv] [-s[server name]] args ...
#
# OPTIONS
#   -s [example.com],--server-name		Set ServerName 	
#   -n [www.example.com],--alt-names		Set Alternative Names
#						- Default to www.${server-name}
#   -d [/srv/www/example.com],--document-root	Set DocumentRoot
#						- Default to 
#						/var/www/vhosts/${server-name}
#   -p [80],--http-port  			Set HTTP port
#						- Default to 80
#
#   --enable-ssl-vhost				Option to enable SSL portion
#   --ssl-port [443]				Set HTTPS port (only used with
#						enable-ssl-vhost)
#						- Default to 443
#   --ssl-certificate-file [/etc/ssl/certs/example.com.crt]
#						Option to specify path to SSL
#						certificate.  This is not
#						optional when enable-ssl-vhost
#						is enabled
#   --ssl-certificate-key-file [/etc/ssl/private/example.com.key]
#						Option to specify path to SSL
#						certificate key file.  This is
#						not optional when 
#						enable-ssl-vhost is enabled
#   --ssl-certificate-ca-file [/etc/ssl/certs/example.com.ca.crt
#						Optional argument to specify
#						a certificate chain file 
#						location when enable-ssl-vhost
#						is enabled
#
#   -z,--no-install				Only print vhost output, do
#						not install.
#   -r,--reload					Reload the Apache service
#   -h, --help					Print help options
#   -v, --version				Print script version
#
# EXAMPLE
#   ${SCRIPT_NAME} -s example.com -n mail.example.com www.example.com -p 81
#
############################################################################### 
# HEADER END
############################################################################### 



#####
# Determine the current distribution and release of the server
function set_distro {
OS=$(python -c "import platform; print(platform.linux_distribution()[0])" | 
     awk '{print tolower($0)}')
RELEASE=$(python -c "import platform; print(platform
                     .linux_distribution()[1])" | awk '{print tolower($0)}')
}

#####
# Print help information
function usage {
cat <<USAGE_TEMPLATE

$(sed -n '/^# USAGE/,/^# EXAMPLE/p' ${0} | sed -e 's/#//' | head -n -1)

USAGE_TEMPLATE
}


#####
# Print version information
function version {
cat <<VERSION_TEMPLATE

 version	"${SCRIPT_NAME}"	0.0.1

VERSION_TEMPLATE
}


#####
# Test to ensure we're running as a privileged user
if [[ "$EUID" -ne 0 ]]; then
  echo "This script must be run as root." >&2
  exit 1
fi

#####
# Parse arguments and options being passed to the script
while getopts ":s:n:d:z:r:v:h" opt; do
  case "${opt}" in
    s) echo "-s was triggered, Parameter: $OPTARG"
       SERVER_NAME="${OPTARG}"
       ;;
    n) SERVER_ALIASES="${OPTARG}"
       ;;
    d) DOCUMENT_ROOT="${OPTARG}"
       ;;
    z) NO_INSTALL=true
       ;;
    r) RELOAD_SERVICE=true
       ;;
    v) version
       exit 0
       ;;
    h) usage
       exit 0
       ;;
    \?) echo "Invalid flag." >&2
        usage
        exit 1 
        ;;
    :) echo "Invalid option for -${OPTARG}." >&2
       usage
       exit 1
       ;;
  esac
done

#####
# Test to ensure the server name was passed to the script
#if ! "${SERVER_NAME}"; then
#  echo "Server name is a required field.  Please re-run the script with
#        the appropriate flags set."
#  usage
#  exit 1
#fi

#####
# Test to ensure certificates are passed if ssl-enable-vhost is selected
if [ "${SSL_ENABLED_VHOST}" = true ]; then
  if [ ! -f "${SSL_CERTIFICATE_FILE}" ] || 
     [ ! -f "${SSL_CERTIFICATE_KEY_FILE}" ]; then
    echo "Please provide a proper SSL Certificate File and SSL Certificate Key
          when enabling the SSL virtual host.  These files must exist in the
          location provided."
    usage
    exit 1
  fi
fi

set_distro
VHOST_DATA="vhost-data-test"
NO_INSTALL=true
if [[ "${OS}" == "centos" ]] || [[ "${OS}" == "redhat" ]]; then
  if [ "${NO_INSTALL}" = true ]; then
    echo "${SERVER_NAME}"
    echo "${VHOST_DATA}"
    exit 0
  fi

  if [ ! -d /etc/httpd/vhost.d ]; then
    mkdir -p /etc/httpd/vhost.d &&
    echo "include vhost.d/*.conf" >> /etc/httpd/conf/httpd.conf
  fi
  echo "${VHOST_DATA}" > /etc/httpd/vhost.d/${SERVER_NAME}.conf
  mkdir -p ${DOCUMENT_ROOT}
  if [ "${RELOAD_SERVICE}" = true ]; then
    apachectl -k graceful &
  fi
elif [[ "${OS}" == "ubuntu" ]] || [[ "${OS}" == "debian" ]]; then
  echo "Debian stuff"
fi
