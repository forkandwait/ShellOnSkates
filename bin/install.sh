#!/usr/bin/env sh
set -e -u

# check we are in the right place in the dir tree (look for programs,
# maybe run something with git). USE BETTER STACK OVERFLOW THING FOR SCRIPT LOCATION
cd ..
echo $(pwd)
DB="$(pwd)/var/SOS.sqlite3"
echo $DB

# check that zip and python3 are availabe


# create database from sql

sqlite3 $DB < ./share/shellonskates.sql

# prime database from pwd and dir structure where install.sh is
# located. delete config first.  install a simple test program.
echo "begin; delete from config; insert into config (base_dir) values '$(pwd)'; commit;" | sqlite3 $DB

# output instructions on how to run
echo "execute the server like this: '$(pwd)/bin/server.py -d $DB'"
echo "execute the queue runner like this (from cron if wanted): '$(pwd)/bin/qr.py -d $DB' "
echo ""
echo "Read the README for more instrutctions."
