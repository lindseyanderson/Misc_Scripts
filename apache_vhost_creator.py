#!/usr/bin/env python

import argparse
import os
import platform
import re
import subprocess
import sys

class Server:
    """
    """
    
    def __init__(self):
        self.distribution = platform.linux_distribution()[0]
        self.version = platform.linux_distribution()[1]
        self.os_family = self.get_family()
        self.apache_binary = "apachectl" if self.os_family is "redhat" else \
                             "apache2ctl"
        self.apache_config_dir = self.get_apache_config_dir()
        self.apache_release_version = self.get_apache_release_version()
        self.apache_vhost_config_dir = self.get_vhost_config_dir()
      
    def enable_virtualhost(self, virtual_host):
        try: 
            if self._os_family == "debian":
                p = subprocess.Popen("a2ensite " + virtual_host, shell=True)
            po = subprocess.Popen(self.apache_binary + " -k graceful", shell=True)
        except:
            print "Could not enable virtual host {0}.".format(virtual_host)
            raise
        return True
        

    def get_vhost_config_dir(self):
        vhost_config_dir = "{0}/vhost.d".format(self.apache_config_dir) if \
                           self.os_family == "redhat" else \
                           "{0}/sites-available".format(self.apache_config_dir)
        return vhost_config_dir

    def get_apache_release_version(self):
        p = subprocess.Popen(self.apache_binary + " -v", shell=True,
                             stdout=subprocess.PIPE)
        for line in p.stdout.readlines():
            if "Server version".lower() in line.lower():
                if "2.2" in line: release = "2.2"
                if "2.4" in line: release = "2.4"
        return release

    def get_apache_config_dir(self):
        apache_base = '/etc/httpd'
        p = subprocess.Popen(self.apache_binary +" -V", shell=True,
                             stdout=subprocess.PIPE)
        for line in p.stdout.readlines():
            if "HTTPD_ROOT" in line:
                apache_base = line.split('=')[1].replace('"', '')
                apache_base = re.sub('[^a-zA-Z0-9-_/.]', '', apache_base)
        if not apache_base: sys.exit(1)
        return apache_base

    def get_family(self):
        self._os_family = 'debian' if self.distribution.lower() == 'debian' \
                          or self.distribution.lower() == 'ubuntu' else \
                          'redhat'
        return self._os_family
   
    def get_distro(self):
        return self._distribution

    def get_distro_release(self):
        return self._version
   
    def print_about(self):
        print "OS Family: {0}".format(self.os_family)
        print "OS Distribution: {0}".format(self.distribution)
        print "OS Release Version: {0}".format(self.version)
        print "Apache Version: {0}".format(self.apache_release_version)
        print "Apache Configuration Base: {0}".format(self.apache_config_dir)
        print "Apache Vhost Configuration Directory: {0}".format(
              self.apache_vhost_config_dir)
   

class VirtualHost:
    """
    """
    def __init__(self, args):
        self._args = args
        self.server_name = self.get_server_name()
        self.server_aliases = self.get_server_aliases() 
        self.document_root = self.get_document_root()

    def get_server_name(self):
        self.server_name = self._args.get('server_name')
        return self.server_name

    def get_server_aliases(self):
        server_aliases = self._args.get('server_aliases')
        self.server_aliases = ' '.join(map(str, server_aliases)) \
                              if server_aliases else \
                              'www.{0}'.format(self.server_name)
        return self.server_aliases
    def get_document_root(self):
        document_root = self._args.get('document_root')
        self.document_root = '/var/www/vhosts/{0}/httpdocs'.format( 
                             self.server_name) if not document_root else \
                             document_root
        return self.document_root


if __name__ == '__main__':
    description = "Virtual Host installation for Apache running on Linux."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-s', '--server-name',
                        help="ServerName to be used in configuration.",
                        required=True)
    parser.add_argument('-a', '--server-aliases', nargs='*',
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
    parser.add_argument('--https-port', default=443,
                        help="HTTPS port for the virtual host to listen on.")
    parser.add_argument('--ssl-certificate-file',
                        help="Location to the SSL Certificate file.")
    parser.add_argument('--ssl-certificate-key-file',
                        help="Location to the SSL Certificate Key file.")
    parser.add_argument('--ssl-certificate-ca-file',
                        help="Location to the SSL Certificate CA file.")
    parser.add_argument('--enable-ssl', action='store_true',
                        help="Enable SSL virtual host.", default=False)

    args = vars(parser.parse_args())

    my_server = Server()
    virtualhost = VirtualHost(args)
    my_server.print_about()
    print virtualhost.server_name
    print virtualhost.server_aliases
    print virtualhost.document_root

