#!/usr/bin/env sh
set -e -u

# check we are in the right place in the dir tree, cd to ONE ABOVE the script
# directory so can find everything else
DIR="$( cd "$( dirname "$0" )" && pwd )"
cd $DIR; cd ..
BASEDIR=$(pwd)

# check that zip and python3 are availabe
command -v zip &>/dev/null || { echo "SOS requires zip but it's not installed. Aborting." >&2; exit 1; }
command -v python3 &>/dev/null || { echo "SOS requires python3 but it's not installed. Aborting." >&2; exit 1; }

# create database from sql and prime from current location
DB="$BASEDIR/var/SOS.sqlite3"
cat ./share/shellonskates.sql | sqlite3 $DB
echo "begin; delete from config; insert into config (base_dir) values ('$BASEDIR/var/tmp'); commit;" | sqlite3 $DB

# write a simple working set of get started commands
EXSCRIPT=example.sh
cat > $EXSCRIPT <<EOF

set -u -e 

# add an analysis with "addanalyis.py".  For example grep with a pattern file:
python3 $BASEDIR/bin/addanalysis.py  -d $BASEDIR/var/SOS.sqlite3 \\
        -a wc1 -c 'grep -H -f patternfile <infile 1>out 2>err' -D 'runs grep on infile with patterns from patternfile'  patternfile infile

# execute the server:
python3 $BASEDIR/cgi/server.py -d $DB

# browse to http://localhost:9999/shellonskates.py
read -p 'Press enter after finished uploading files'

# execute the queue runner (from cron if wanted):
python3 $BASEDIR/bin/qr.py -d $DB

EOF

#  finis
printf "SUCCESS!!  Look in $EXSCRIPT to see a set of installation commands.  Read the README.\n\n"
