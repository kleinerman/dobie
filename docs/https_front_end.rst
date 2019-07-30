Generating SSL certificates to let the front end run under https
================================================================

.. contents::

Generate the private key of the CA
----------------------------------

.. code-block::

  # openssl genrsa -out dobie_ca.key 2048


Generate the certificate of the CA
----------------------------------

.. code-block::

  # openssl req -x509 -new -nodes -key dobie_ca.key -sha256 -days 7300 -out dobie_ca.crt


The following things will be asked:

.. code-block::

  Country Name (2 letter code) [AU]:AR
  State or Province Name (full name) [Some-State]:Cordoba
  Locality Name (eg, city) []:Cordoba
  Organization Name (eg, company) [Internet Widgits Pty Ltd]:Dobie
  Organizational Unit Name (eg, section) []:Dobie
  Common Name (e.g. server FQDN or YOUR name) []:server.dobie
  Email Address []:jkleinerman@gmail.com


Configuration of the server certificate
---------------------------------------

In the same folder create a file ``server.conf`` with the following content:

.. code-block::

  [req]
  default_bits = 2048
  prompt = no
  default_md = sha256
  distinguished_name = dn

  [dn]
  C=AR
  ST=Cordoba
  L=Cordoba
  O=Dobie
  OU=Dobie
  emailAddress=jkleinerman@gmail.com
  CN=server.dobie


In the same folder create a file ``server.conf`` with the following content:

.. code-block::

  authorityKeyIdentifier=keyid,issuer
  basicConstraints=CA:FALSE
  keyUsage=digitalSignature,nonRepudiation,keyEncipherment,dataEncipherment
  subjectAltName=@alt_names

  [alt_names]
  DNS.1=server.dobie



Server private key
------------------

Generate it doing:

.. code-block::

  # openssl req -new -sha256 -nodes -out server.csr -newkey rsa:2048 -keyout server.key -config <( cat server.conf )


Server certificate
------------------

Generate it doing:

.. code-block::

  # openssl x509 -req -in server.csr -CA dobie_ca.crt -CAkey dobie_ca.key -CAcreateserial -out server.crt -days 7300 -sha256 -extfile v3.ext


Diffie-Hellman parameters
-------------------------

While we are using OpenSSL, we should also create a strong Diffie-Hellman group, which is used in negotiating Perfect Forward Secrecy with clients.

.. code-block::

  # openssl dhparam -out dhparam.pem 4096


Nginx Configuration
-------------------

Nginx need the following three files: 

.. code-block::

  - server.key
  - server.crt
  - dhparam.pem

They should be saved in the directory ``dobie/server/docker/webserver/`` of the repo.

These files should be pointed by Nginx configuration file that also is located in the same directory:

.. code-block::

  server {
      listen       80;
      listen  [::]:80;
      server_name  localhost;

      location / {
          rewrite ^ https://$host$request_uri? permanent;
      }

  }


  server {
      listen 443 ssl http2;
      listen [::]:443 ssl http2;
      server_name localhost;

      # Don't send the nginx version number in error pages and Server header
      server_tokens off;

      ssl_certificate /etc/nginx/ssl/server.crt;
      ssl_certificate_key /etc/nginx/ssl/server.key;

      ssl_buffer_size 8k;

      # Diffie-Hellman parameter for DHE ciphersuites.
      ssl_dhparam /etc/nginx/ssl/dhparam.pem;

      # Disable SSLv3 (enabled by default since nginx 0.8.19). It's less secure then TLS
      ssl_protocols TLSv1.2 TLSv1.1 TLSv1;

      # Specifies that server ciphers should be preferred over client ciphers when using 
      # the SSLv3 and TLS protocols. It's used to protect from BEAST attack
      ssl_prefer_server_ciphers on;

      # Specifies the enabled ciphers
      ssl_ciphers ECDH+AESGCM:ECDH+AES256:ECDH+AES128:DH+3DES:!ADH:!AECDH:!MD5;

      ssl_ecdh_curve secp384r1;

      ssl_session_tickets off;
      
      root /site;
      index index.php index.html index.htm;

      location / {
          if (!-e $request_filename) {
              rewrite ^(.*)$ /$1.php;
          }
      }

      #error_page  404              /404.html;

      # redirect server error pages to the static page /50x.html
      error_page   500 502 503 504  /50x.html;
      location = /50x.html {
          root   /usr/share/nginx/html;
      }

      location ~ \.php$ {
          fastcgi_pass   php:9000;
          fastcgi_index  index.php;
          fastcgi_param  SCRIPT_FILENAME  $document_root$fastcgi_script_name;
          include        fastcgi_params;
      }
  }


| In the same file is done the configuration to redirect http (port 80) to https (port 443).
| In this file also is configured some things related with PHP and the root of the site is confiured to point the the place where dobie site is located.


Applying all this to Nginx Docker container
-------------------------------------------

All the above files should be copied to the container. This is done in the Dockerfile which is in the same directory.


Web Browser configuration
-------------------------

| To avoid web browser complain, install the CA certificate on it.
| In **Goolge Chrome**, go to Settings, Advanced, Manage certificates, Authorities (tab) and import the file ``dobie_ca.crt`` previously generated.
| In **Firefox**, go to Preferences, Privacy & Security, Certificates, and press "View Certificates..." button, press "Import" button and select the file ``dobie_ca.crt`` previously generated.
| In both browsers, always access to the front end using the FQDN: ``http://server.dobie``. To do that configure your ``/etc/hosts`` file to point to the server IP:



.. code-block::

  10.10.7.79   server.dobie