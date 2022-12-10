# Configure SSH on a new Ubuntu 16.04 machine

file_line { 'PasswordAuthentication':
  path => '/etc/ssh/ssh_config',
  line => 'PasswordAuthentication no'
}

file_line { 'IdentityFile':
  path => '/etc/ssh/ssh_config',
  line => 'IdentityFile ~/.ssh/holberton'
}

file_line { 'GSSAPIAuthentication':
  path => '/etc/ssh/ssh_config',
  line => 'GSSAPIAuthentication yes'
}
