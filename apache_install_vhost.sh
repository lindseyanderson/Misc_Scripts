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
#   -r,--reload					Reload the Apache service
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
while getopts ":v:h" opt; do
  case "${opt}" in
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
