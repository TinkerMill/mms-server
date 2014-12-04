host {"dooraccess":
  ip => "192.168.0.30",
}

package {"mysql-server":
  ensure  => latest,
  require => [ Exec["dbpass1"], Exec["dbpass2"] ],

  }

package {"python-pip":
  ensure => latest,
}

package {"git":
  ensure => latest,
  }

package {"python-mysqldb":
  ensure => latest,
}

exec{"dbpass1":
  command => "/bin/echo mysql-server mysql-server/root_password password strangehat | /usr/bin/debconf-set-selections"
}

exec{"dbpass2":
  command => "/bin/echo mysql-server mysql-server/root_password_again password strangehat | /usr/bin/debconf-set-selections"
}

exec {"flask":
  command => "/usr/bin/pip install flask"
  require => Package['python-pip'],
  }

exec {"Flask-SQLAlchemy":,
  command => "/usr/bin/pip install Flask-SQLAlchemy"
  require => Package['python-pip'],
  }

exec {"SQLAlchemy":
  command => "/usr/bin/pip install SQLAlchemy",
  require => Package['python-pip'],
}

exec {"createDB":
  command => 'echo "create database if not exists mms_server" | mysql --user=root --password=strangehat'}
  require => Package['mysql-server'],
}
