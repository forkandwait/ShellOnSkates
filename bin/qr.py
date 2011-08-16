#!/usr/local/bin/python3

## blah imports blah
import os
import shlex
import sqlite3
import subprocess
import sys
import tempfile
import time
import uuid

## start up -- connect to db XXX grab from command line
conn = sqlite3.connect('/Users/webbs/PROJECTS/SHELL_ON_SKATES/SOS.sqlite3')
cur = conn.cursor()

## go to reasonable base directory
base_dir = cur.execute('select base_dir from config limit 1;').fetchone()[0]
if base_dir is None:
    sys.stderr.write('no base dir in config sql table -- exiting.')
    exit(1)
os.chdir(base_dir)  # XXX don't do anything here yet

# check other qr's running, claim if not
_pid = os.getpid()
qrpid = cur.execute('select pid, start_time from qrstate where finish_time is null').fetchone()
if qrpid is None:
    cur.execute('insert into qrstate (pid) values (?)', (_pid,))
else:
    sys.stderr.write('qr already running: pid=%i, start_time=%s.  Exiting\n' % qrpid);
    exit (1)

## big loop to clear the queue, update state as progress, exit if empty
while True:

    # get most recent request from queue table, exit loop if empty
    _sql = 'select run_id, analysis_id, run_dir from queue where run_exitcode is null order by run_pushtime desc limit 1;'
    run_current = cur.execute(_sql).fetchone()
    if run_current is None:
        break
    else: 
        (run_id, analysis_id, run_dir) = run_current

    # update qrstate
    cur.execute('update qrstate set current_runid = ?;', (run_id,))
    cur.execute('update qrstate set current_runstate = ?;', ('RUNNING',))

    # do analysis -- use call() because Popen is too object oriented and lame
    commandstr = cur.execute('select commandstr from analyses where analysis_id = ?;', (analysis_id,)).fetchone()[0]
    sys.stderr.write('running %s (%s)\n' % (commandstr, run_id))
    os.chdir(run_dir)
    rc = subprocess.call(commandstr, shell=True);    
    cur.execute('update queue set run_finishtime=current_timestamp, run_exitcode=? where run_id = ?;', (rc, run_id))
    sys.stderr.write('ran %s (%s) with return code %i.  zipping results.\n' % (commandstr, run_id, rc))

    # if ok, zip up results, save in db, update state tables
    os.chdir('..')
    sys.stderr.write(os.getcwd()+"\n")
    cur.execute('update qrstate set current_runstate = ?;', ('ZIPPING',))
    zipcommand = "zip -r '%s/%s' '%s'" % (base_dir, run_id, os.path.basename(run_dir))
    sys.stderr.write(zipcommand + "\n")
    p = subprocess.Popen(shlex.split(zipcommand))
    #p = subprocess.Popen(shlex.split("tar cvzf %s/%s.tar.gz '%s'" % (base_dir, run_id, run_dir)))    
    rc = p.wait()
    if rc != 0:
        raise Exception('Non zero return code from zip: %i' % rc)
    else:
        cur.execute('update qrstate set current_runstate = ?;', (None,)) 
        cur.execute('update qrstate set current_runid = ?;', (None,))
        with open("%s/%s.zip" % (base_dir, run_id), "rb") as input_file:
            ablob = input_file.read()
            cur.execute("update queue set results = ? where run_id = ?", [sqlite3.Binary(ablob), run_id])
        pass
    sys.stderr.write('finished zipping %s (%s).\n' % (commandstr, run_id))


    # XXX cd to base directory
    #os.chdir(base_dir)
    
    ## commit this run's changes
    conn.commit()
    
    pass

## clean up, summarize
cur.execute('update qrstate set finish_time = current_timestamp where pid = ?;', (_pid,))
conn.commit()
exit(0)
