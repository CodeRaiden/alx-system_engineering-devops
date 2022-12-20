# Install & configure NGINX on a new Ubuntu 16.04 server

$index_html = "\
<html>
  <head>
    <title>Hello World!</title>
  </head>
  <body>
    <p>Hello World!</p>
  </body>
</html>
"

$custom_404 = "\
<html>
  <head>
    <title>Page Not Found</title>
  </head>
  <body>
    <p>Ceci n'est pas une page</p>
  </body>
</html>
"

exec { 'apt update':
  path => '/usr/sbin:/usr/bin:/sbin:/bin',
}

package { 'nginx':
  ensure  => 'installed',
  require => Exec['apt update'],
}

service { 'nginx':
  ensure     => 'running',
  enable     => true,
  hasrestart => true,
  require    => Exec['default_conf'],
}

exec { 'default_conf':
  command => "sed -i '/^\\troot \\/var\\/www\\/html;$/a rewrite ^/redirect_me https://www.google.com permanent; error_page 404 /custom_404.html; location = /custom_404.html { root /usr/share/nginx/html; internal; }' /etc/nginx/sites-available/default",
  path    => '/usr/sbin:/usr/bin:/sbin:/bin',
  require => Package['nginx'],
}

exec { 'custom_response_header':
  command => "sed -i '/^http {$/a add_header X-Served-By ${::hostname};' /etc/nginx/nginx.conf",
  path    => '/usr/sbin:/usr/bin:/sbin:/bin',
  require => Package['nginx'],
}

file { '/var/www/html/index.html':
  ensure  => present,
  replace => 'no',
  content => $index_html,
  require => Package['nginx'],
}

file { '/usr/share/nginx/html/custom_404.html':
  ensure  => present,
  replace => 'no',
  content => $custom_404_html,
  require => Package['nginx'],
}

exec { "ufw allow 'Nginx HTTP'":
  path    => '/usr/sbin:/usr/bin:/sbin:/bin',
  require => Package['nginx'],
}
