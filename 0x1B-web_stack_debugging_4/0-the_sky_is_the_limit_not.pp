# Increase file descriptor limit for NGINX

service {'nginx':
  ensure => running
}

exec {'sed -E -i \'s/^(ULIMIT=.*-n)[ \t]+[0-9]+\>/\1 1024/\' /etc/default/nginx':
  path   => '/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin',
  notify => Service['nginx']
}
