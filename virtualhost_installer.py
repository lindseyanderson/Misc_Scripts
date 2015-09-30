#!/usr/bin/env python

import argparse
import platform


apache_http22_template = """<VirtualHost {bind_address}:{http_port}>
        ServerName {server_name} 
        ServerAlias {alt_names}
        DocumentRoot {document_root}

        <Directory {document_root}>
                Options -Indexes +FollowSymLinks -MultiViews
                AllowOverride All
		Order deny,allow
		Allow from all
        </Directory>
        CustomLog {log_directory}/{server_name}.access.log combined
        ErrorLog {log_directory}/{server_name}-error.log
        # Possible values include: debug, info, notice, warn, error, crit,
        # alert, emerg.
        LogLevel warn
        {ssl_options}
</VirtualHost>"""

apache_http22_ssl_options = """
        SSLEngine on
        SSLCertificateFile    {ssl_certificate_file} 
        SSLCertificateKeyFile {ssl_certificate_key_file}
        {ssl_certificate_ca_file}

        <FilesMatch \"\.(cgi|shtml|phtml|php)$\">
                SSLOptions +StdEnvVars
        </FilesMatch>

        BrowserMatch \"MSIE [2-6]\" \
                nokeepalive ssl-unclean-shutdown \
                downgrade-1.0 force-response-1.0
        BrowserMatch \"MSIE [17-9]\" ssl-unclean-shutdown
"""


def distro_log_dir():
    distro_log_dir = "/var/log"
    if (platform.linux_distribution()[0].lower() == "centos") or \
       (platform.linux_distribution()[0].lower() == "redhat"):
        distro_log_dir = "/var/log/httpd"
    elif (platform.linux_distribution()[0].lower() == "debian") or \
         (platform.linux_distribution()[0].lower() == "ubuntu"):
        distro_log_dir = "/var/log/apache2"
    return distro_log_dir

def create_template(args):
    template = ''
    args['ssl_options'] = ''
    args['log_directory'] = distro_log_dir() if not \
         args.get('log_directory') else args.get('log_directory')
    args['document_root'] = '/var/www/vhosts/{0}'.format(
         args.get('server_name')) if not args.get('document_root') else \
         args.get('document_root')
    args['alt_names'] = ' '.join(map(str, args.get('alt_names')))
    if args.get('ssl_enabled'):
        args['ssl_enabled'] = False
        template = create_template(args)
        args['ssl_options'] = apache_http_template.format(**args)

    template = template + apache_http22_template.format(**args) 
    return template

if __name__ == '__main__':

    description = "Installer of virtual hosts for various services"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-s', '--server-name',
                        help="ServerName to be used in configuration.",
                        required=True)
    parser.add_argument('-n', '--alt-names', nargs='*',
                        help="List of alternate names")
    parser.add_argument('-d', '--document-root', 
                        help="Location for all files to be stored.")
    parser.add_argument('-b', '--bind-address', default='*',
                        help="IP the virtual host will listen on.")
    parser.add_argument('-l', '--log-directory',
                        help="Log directory location on the server.")
    parser.add_argument('-p', '--http-port', 
                        help="HTTP port for the virtual host to listen on.",
                        default=80)
    parser.add_argument('-r', '--reload-service', action='store_true',
                        help="Reload the service after installation.",
                        default=False)
    parser.add_argument('-z', '--no-install', action='store_true',
                        help="Only display virtual host data, do not install.",
                        default=False)

    args = vars(parser.parse_args())
    os_distribution = platform.linux_distribution()[0].lower()
    os_release = platform.linux_distribution()[1].lower()

    print create_template(args) if args.get('no_install') else install_vhost(args)
