#!/usr/bin/env python3

## Imports
import cgitb; cgitb.enable() 
import cgi
import http.cookies as cookies
import os
import sqlite3
import tempfile
import sys
import uuid


## Real code....
if __name__ == '__main__':
    # check for main database, exit if not present.  Use envar so can be fired by 
    DB = os.getenv('SOS_DB')
    if not DB:
        sys.stderr.write("Missing envar for SOS_DB.")
        exit(1)
    if not os.path.isfile(DB) or not DB:
        sys.stderr.write("Could not find database.  Tried: '%s'." % DB)
        exit(1)

    ## link string to appended to lots of pages
    linkstr =  "<hr>\n"
    linkstr += "<a href=./shellonskates.py?task=listanalyses>List Analyses</a><br/>\n"
    linkstr += "<a href=./shellonskates.py?task=listruns>List Runs</a><br/>\n"

    # get cgi stuff into standard variables
    formdata = cgi.FieldStorage()

    # no task parameter -- 
    if 'task' not in formdata.keys() or  formdata['task'].value == 'listanalyses':
        ## links to all the output of finished runs (zipped).  Status
        ## of running analyses
        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        print("Content-type: text/html;\n\n")    
        for row in cur.execute('select analysis_id, description from analyses order by analysis_id;'): 
            print("analysis_id: <a href=shellonskates.py?task=showform&analysis_id=%s>%s</a> - %s <br>\n" % (row[0], row[0], row[1]))
            pass
        print(linkstr)
        exit(0)
        

    elif formdata['task'].value == 'enqueue':
        # connect to db
        conn = sqlite3.connect(DB)
        cur = conn.cursor()

        # from form data, read analysis id, verify in database, exit if not
        if 'analysis_id' not in formdata.keys():
            print("Content-type: text/html;\n\n")    
            print ('<h2>Error -- no "analysis_id" parameter in submission</h2>')
            print(linkstr)
            exit(0)
        else:
            a_id = str(formdata['analysis_id'].value) 
        cur.execute("select count(*) from analyses where analysis_id = ?", [a_id])
        if cur.fetchone()[0] == 0:
            print("Content-type: text/html;\n\n")    
            print ("<h2>Error -- no such analysis available ('%s')</h2>\n" % a_id)
            print(linkstr)
            exit (0) 

        # start new run:  push new run-id + analysis name onto queue in db, mk temp dir
        run_id = str(uuid.uuid4())
        a_id = str(formdata['analysis_id'].value) 
        descrip = str(formdata['description'].value) 
        
        run_dir = tempfile.mkdtemp() 
        cur.execute('insert into queue (run_id, run_dir, analysis_id, description) values (?, ?, ?, ?);',
                    [run_id, str(run_dir), a_id, descrip]) 

        # Grab all the form data and either store files in the
        # directory or form values in a keyvalue table.  XXX Bunch of
        # crap to test the various string "types" the data come in
        for fieldname in formdata.keys(): 
            if str(type(formdata[fieldname].file)) in ["<class '_io.BytesIO'>", "<class '_io.BufferedRandom'>"]:  # XXX wtf?
                ## if file upload
                if formdata[fieldname].done == -1:
                    print("Content-type: text/html;\n\n")    
                    print ('<h2>Error -- stopped datafile upload</h2>')
                    print(linkstr)        
                    exit(0)
                f = open(run_dir + '/' + fieldname, 'wb')
                data = (formdata[fieldname].value)
                f.write(data)
                f.close() 
            
            elif str(type(formdata[fieldname].file)) == "<class '_io.StringIO'>":
                ## if form key/ value input
                cur.execute('insert into formkv (run_id, k, v) values (?, ?, ?);',
                            [str(run_id), str(fieldname), str(formdata[fieldname].value)])
            else:
                ## Junk
                print("Content-type: text/html;\n\n")    
                print ("Error due to lame checking of file upload. View source to diagnose overcompulsive \"pythonic\" typing. Fieldname == %s" % str(fieldname))
                print(linkstr) 
        # clean up and exit
        conn.commit()
        cur.close()
        print("Content-type: text/html;\n\n")    
        print("Successfully submitted analysis.<br>\n run_id: %s<br>\nrun_dir: %s\n<br>analysis_id: %s<br>\n" % (run_id, run_dir, a_id))
        print(linkstr) 

        exit(0)
        pass

    elif formdata['task'].value == 'listruns':
        ## links to all the output of finished runs (zipped).  Status
        ## of running analyses
        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        print("Content-type: text/html;\n\n")    
        print("<table><tr><th>Analysis<th>Push Time<th>Notes<th>Description<tr/>")
        sql = 'select run_id, analysis_id, run_pushtime, run_finishtime, description from queue order by run_pushtime desc'
        for row in cur.execute(sql): 
            if row[3] is None:
                print("<tr><td>%s<td>%s<td>PENDING<td>%s</tr>\n" % (row[1], row[2], row[4])) 
            else:
                print("<tr><td>%s<td>%s<td>FINIS<td><a href=shellonskates.py?task=downloadresults&run_id=%s>%s</a></tr>\n" % \
                          (row[1], row[2], row[0], row[4]))
            pass
        print ("</table>")
        print(linkstr) 
        exit(0)

    elif formdata['task'].value == 'showform':
        ## show form -- simple file upload, dropdown with all analyses
        # connect to db
        conn = sqlite3.connect(DB)
        cur = conn.cursor()

        # from form data, read analysis id, verify in database, exit if not
        if 'analysis_id' not in formdata.keys():
            print("Content-type: text/html;\n\n")    
            print ('<h2>Error -- no "analysis_id" parameter in submission</h2>')
            exit(0)
        else:
            a_id = str(formdata['analysis_id'].value) 
        cur.execute("select count(*) from analyses where analysis_id = ?", [a_id])
        if cur.fetchone()[0] == 0:
            print("Content-type: text/html;\n\n")    
            print ("<h2>Error -- no such analysis available ('%s')</h2>\n" % a_id)
            exit (0) 
        
        ## it's all good -- display the form
        formstr = cur.execute('select htmlform from analyses where analysis_id = ?;', [a_id]).fetchone()[0]
        print("Content-type: text/html;\n\n")    
        print (formstr)
        print(linkstr) 
        exit(0)
        pass 
    elif formdata['task'].value == 'downloadresults':
        if 'run_id' not in formdata.keys():
            print("Content-type: text/html;\n\n")    
            print('<h2>Error -- need run_id to download results</h2>\n');
            exit(0)
        else:
            run_id = formdata['run_id'].value
        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        cur.execute("select results, analysis_id from queue where run_id = ?", [run_id])
        _res = cur.fetchone()
        results = _res[0]
        analysis_id = _res[1]
        if results is None:
            print("Content-type: text/html;\n\n")    
            print ('<h2>Invalid run_id: "%s"</h2>' % (run_id,))
            exit(0)
        else:
            ## download the zipfile, (bunch of crap to sabotage unicode, otherwise get garbage in the download binary)
            header = "Content-type: application/zip;\n"
            header += "Content-length: %d\n" % len(results)
            header += "Content-Disposition: attachment; filename=%s-%s.zip\n" % (analysis_id, run_id)
            header += "\n"
            sys.stdout.buffer.write(header.encode('ascii'))
            sys.stdout.flush()
            sys.stdout.buffer.write(results); 
            sys.stdout.flush()
        exit(0)
        pass 

    else:
        print ("<h2>Unknown task: %s" % formdata['task'].value)
        print(linkstr) 
        exit(0)
