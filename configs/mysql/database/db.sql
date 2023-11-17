-- create databases
CREATE DATABASE IF NOT EXISTS `liquefier`;

-- create root user and grant rights
GRANT ALL ON *.* TO 'root'@'%';
GRANT RELOAD, SHOW DATABASES, REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'root'@'%';