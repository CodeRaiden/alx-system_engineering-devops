# Removed limits for user 'holberton'
exec {'sed -E -i \'s/^holberton\>/#&/\' /etc/security/limits.conf':
  path => '/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin'
}
