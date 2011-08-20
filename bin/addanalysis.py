#!/usr/bin/env python3
## imports                                                                                                                                        
import argparse
import os
import sqlite3
import sys

## parse args
parser = argparse.ArgumentParser(description='Install a new analysis in SOS.')
parser.add_argument('--db', '-d', type=str, help='Database', required=True)
parser.add_argument('--analysis_id', '-a', type=str, help='analysis ID (short, no spaces)', required=True)
parser.add_argument('--commandstr', '-c', type=str, help='command string (use quotes)', required=True)
parser.add_argument('--docstr', '-D', type=str, help='doc string (use quotes)', required=True)
parser.add_argument('filenames', metavar='N', type=str, nargs='+', help='filenames for the form')
args = parser.parse_args()

## create form from filenames args
htmlstuff = "<title> %s Form</title>" % args.analysis_id
htmlstuff += '<form action="shellonskates.py" ENCTYPE="multipart/form-data"  method="post">'
htmlstuff += '\t\t<input type="hidden" name="task" value="enqueue">\n'
htmlstuff += '\t\t<input type="hidden" name="analysis_id" value="%s">\n' % args.analysis_id
for fname in args.filenames:
    htmlstuff += '\t\tFile to upload (%s): <input name="%s" type="file" size=0> <br>\n' % (fname, fname)
htmlstuff += ''' 
\t\t<hr>
\t<input type="text" value="Description"/><br>
\t<input type="submit" value="Submit"/><br>
<p>Description: "%s" </p>
</form> ''' % args.docstr

## connect to database
conn = sqlite3.connect(args.db)
cur = conn.cursor()

## insert, finish
cur.execute('insert into analyses (analysis_id, commandstr, htmlform, description) values (?, ?, ?, ?)', [args.analysis_id, args.commandstr, htmlstuff, args.docstr])
conn.commit()
conn.close()
exit(0) 
