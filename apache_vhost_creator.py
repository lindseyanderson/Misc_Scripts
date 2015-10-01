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
   

if __name__ == '__main__':
    my_server = Server()
    my_server.print_about()
