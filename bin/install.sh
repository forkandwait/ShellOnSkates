#!/usr/bin/env sh
set -e -u

# check we are in the right place in the dir tree, cd to ONE ABOVE the script
# directory so can find everything else
DIR="$( cd "$( dirname "$0" )" && pwd )"
cd $DIR
cd ..
BASEDIR=$(pwd)

# check that zip and python3 are availabe
command -v zip &>/dev/null || { echo "SOS requires zip but it's not installed. Aborting." >&2; exit 1; }
command -v python3 &>/dev/null || { echo "SOS requires python3 but it's not installed. Aborting." >&2; exit 1; }

# create database from sql and prime from current location
DB="$BASEDIR/var/SOS.sqlite3"
cat ./share/shellonskates.sql | sqlite3 $DB
echo "begin; delete from config; insert into config (base_dir) values ('$BASEDIR/tmp'); commit;" | sqlite3 $DB

# output instructions on how to run
printf "SUCCESS\n\n"
printf "add an analysis with \"addanalyis.py\":\n\t 'python3 $BASEDIR/bin/addanalysis.py --help'\n\n"
printf "execute the server like this:\n\t 'python3 $BASEDIR/cgi/server.py -d $DB'\n\n"
printf "execute the queue runner like this (from cron if wanted):\n\t 'python3 $BASEDIR/bin/qr.py -d $DB' \n\n"
printf "Read the README for more information.\n"
