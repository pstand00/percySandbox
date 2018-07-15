-- connect as root
-- mysql -h mysandbox.cna2cedqzaal.us-east-1.rds.amazonaws.com -P 3306 -u root -p
-- above doesnt work

-- connect to data base 
mysql -h mysandbox.cna2cedqzaal.us-east-1.rds.amazonaws.com -P 3306 -u pstandbridge -p
mysql -h mysandbox.cna2cedqzaal.us-east-1.rds.amazonaws.com -P 3306 -u pete -p 

-- create user 
CREATE USER 'pete'@'%' IDENTIFIED BY 'Password1';

-- grant specific priveleges to users 
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, RELOAD, PROCESS, REFERENCES, INDEX, ALTER, SHOW DATABASES, CREATE TEMPORARY TABLES, LOCK TABLES, EXECUTE, REPLICATION SLAVE, REPLICATION CLIENT, CREATE VIEW, SHOW VIEW, CREATE ROUTINE, ALTER ROUTINE, CREATE USER, EVENT, TRIGGER ON *.* TO 'pete'@'%' WITH GRANT OPTION;
GRANT all ON *.* TO 'pete'@'%' WITH GRANT OPTION;

-- quit mySql instance
quit

-- list databases in the server
show databases;

-- create database named 'testDb'
create database if not exists testDb;

-- connect to a specific db
use testDb;

-- show tables
show tables;

-- drop table 
drop table if exists testTable;

-- create table
create table testTable (id int, colA varchar(25), colB varchar(20));

-- get table structure
describe testTable;

-- insert a row 
insert into testTable values (1, 'Value 1', "4.8");
insert into testTable values (2, 'Value 2', "6.4");