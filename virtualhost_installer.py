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
        CustomLog {log_string}.access.log combined
        ErrorLog {log_string}-error.log
        # Possible values include: debug, info, notice, warn, error, crit,
        # alert, emerg.
        LogLevel warn
        {ssl_options}
</VirtualHost>
"""

apache_http22_ssl_options = """
        SSLEngine on
        SSLCertificateFile    {ssl_certificate_file} 
        SSLCertificateKeyFile {ssl_certificate_key_file}
        {ssl_certificate_ca_file}

        <FilesMatch \\"\.(cgi|shtml|phtml|php)$\\">
                SSLOptions +StdEnvVars
        </FilesMatch>

        BrowserMatch \\"MSIE [2-6]\\" \\
                nokeepalive ssl-unclean-shutdown \\
                downgrade-1.0 force-response-1.0
        BrowserMatch \\"MSIE [17-9]\\" ssl-unclean-shutdown
"""

def get_log_string(args):
    log_string = '/var/log/{0}/ssl-{1}' if args.get('enable_ssl') \
                 else '/var/log/{0}/{1}'
    if (platform.linux_distribution()[0].lower() == "centos") or \
       (platform.linux_distribution()[0].lower() == "redhat"):
        log_string = log_string.format('httpd', args.get('server_name'))
    elif (platform.linux_distribution()[0].lower() == "ubuntu") or \
         (platform.linux_distribution()[0].lower() == "debian"):
        log_string = log_string.format('apache2', args.get('server_name'))
    else:
        log_string = log_string.format('apache2', args.get('server_name'))
    return log_string

def create_template(args):
    template = ''
    args['document_root'] = '/var/www/vhosts/{0}/httpdocs'.format(
         args.get('server_name')) if not args.get('document_root') else \
         args.get('document_root')
    log_string = get_log_string(args)
    if args.get('enable_ssl'):
        args['enable_ssl'] = False
        template = create_template(args)
        args['enable_ssl'] = True
        args['ssl_certificate_ca_file'] = 'SSLCACertificateFile  {0}'.format(
             args.get('ssl_certificate_ca_file')) if \
             args.get('ssl_certificate_ca_file') else ''
        args['http_port'] = args.get('https_port')
        args['ssl_options'] = apache_http22_ssl_options.format(**args)

    args['log_string'] = log_string if not \
        args.get('log_string') else args.get('log_string')
    template = template + apache_http22_template.format(**args) 
    args['log_string'] = None
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
    parser.add_argument('--https-port', default=443,
                        help="HTTPS port for the virtual host to listen on.")
    parser.add_argument('--ssl-certificate-file',
                        help="Location to the SSL Certificate file.")
    parser.add_argument('--ssl-certificate-key-file',
                        help="Location to the SSL Certificate Key file.")
    parser.add_argument('--ssl-certificate-ca-file',
                        help="Location to the SSL Certificate CA file.")
    parser.add_argument('-r', '--reload-service', action='store_true',
                        help="Reload the service after installation.",
                        default=False)
    parser.add_argument('-z', '--no-install', action='store_true',
                        help="Only display virtual host data, do not install.",
                        default=False)
    parser.add_argument('--enable-ssl', action='store_true',
                        help="Enable SSL virtual host.", default=False)

    args = vars(parser.parse_args())
    if args.get('enable_ssl') and args.get('ssl_certificate_file') is None \
       and args.get('ssl_certificate_key_file') is None:
        parser.error('--enable-ssl requires --ssl-certificate-file and '
                     '--ssl-certificate-key-file.')
    args['alt_names'] = ' '.join(map(str, args.get('alt_names')))
    args['ssl_options'] = ''

    print create_template(args) if args.get('no_install') else install_vhost(args)