# Misc_Scripts
======
### Vhost Installation - Usage
```
usage: apache_vhost_creator.py [-h] -s SERVER_NAME
                               [-a [SERVER_ALIASES [SERVER_ALIASES ...]]]
                               [-d DOCUMENT_ROOT] [-b BIND_ADDRESS]
                               [-l LOG_DIRECTORY] [-p HTTP_PORT] [-r] [-z]
                               [--https-port HTTPS_PORT]
                               [--ssl-certificate-file SSL_CERTIFICATE_FILE]
                               [--ssl-certificate-key-file SSL_CERTIFICATE_KEY_FILE]
                               [--ssl-certificate-ca-file SSL_CERTIFICATE_CA_FILE]
                               [--enable-ssl] [--verbose]

Virtual Host installation for Apache running on Linux.

optional arguments:
  -h, --help            show this help message and exit
  -s SERVER_NAME, --server-name SERVER_NAME
                        ServerName to be used in configuration.
  -a [SERVER_ALIASES [SERVER_ALIASES ...]], --server-aliases [SERVER_ALIASES [SERVER_ALIASES ...]]
                        List of alternate names
  -d DOCUMENT_ROOT, --document-root DOCUMENT_ROOT
                        Location for all files to be stored.
  -b BIND_ADDRESS, --bind-address BIND_ADDRESS
                        IP the virtual host will listen on.
  -l LOG_DIRECTORY, --log-directory LOG_DIRECTORY
                        Log directory location on the server.
  -p HTTP_PORT, --http-port HTTP_PORT
                        HTTP port for the virtual host to listen on.
  -r, --reload-service  Reload the service after installation.
  -z, --no-install      Only display virtual host data, do not install.
  --https-port HTTPS_PORT
                        HTTPS port for the virtual host to listen on.
  --ssl-certificate-file SSL_CERTIFICATE_FILE
                        Location to the SSL Certificate file.
  --ssl-certificate-key-file SSL_CERTIFICATE_KEY_FILE
                        Location to the SSL Certificate Key file.
  --ssl-certificate-ca-file SSL_CERTIFICATE_CA_FILE
                        Location to the SSL Certificate CA file.
  --enable-ssl          Enable SSL virtual host.
  --verbose             Enable Verbose output.
```
