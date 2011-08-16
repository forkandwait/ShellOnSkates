

# config parameters -- maybe write a config file that is used, then an
# install that reads it.  This assumes that config stuff will be
# stored in the db.

SOS_USERNAME='webbs'
SOS_FILESPACE_DIR='/Users/webbs/SOS'
SOS_CGI_DIR='/usr/local/apache/cgi-bin/webbs/sos'
SOS_ANALYSES_DIR="$SOS_CGI_DIR/ANALYSES"
SOS_RUNS_DIR='/tmp/sos_runs'
SOS_DB="$SOS_CGI_DIR/sos.sqlite3"
SOS_USER='webbs'
SOS_QR_DIR='/usr/local/bin'

# test that destinations are installable, exit and report if not

# make dirs, symlink so cgi executables can find them, and copy executables

# create database from config things and sql skeleton, copy
# appropriate location

# create sample projects and install in appropriate locations.  Insert
# into db config info.

# update cron tab or make appropriate line available (interactively
# like git with vi?) Probably just write something that goes into the
# background



# report

# exit
