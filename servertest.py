#!/usr/bin/env python3

'''*** **************************************************************
    
    PROGRAM: 
    
    DESCRIPTION: Runs a simple cgi server with environment to allow
        for shellonskates.py
    
    PROGRAMMERS:  webb.sprague@ofm.wa.gov    
    
    DATE STARTED: 2011-08-14

    NOTES:  TODO: Add recovery code (try, catch, etc)
    
**********************************************************************************'''
## imports
import os
import sys
from http.server import HTTPServer, CGIHTTPRequestHandler

## Default configs -- I thought 
os.environ['SOS_DB']='/Users/webbs/PROJECTS/SHELL_ON_SKATES/var/SOS.sqlite3'
#os.putenv('SOS_DB', '/Users/webbs/PROJECTS/SHELL_ON_SKATES/var/SOS.sqlite3')
PORT = 9999

## set up and fire off cgi server, recovering 
class Handler(CGIHTTPRequestHandler):
    cgi_directories = ["/cgi"]
httpd = HTTPServer(("", PORT), Handler)
sys.stderr.write("serving at port: %i, home dir: %s\n" %(PORT, os.getcwd()))
sys.stderr.flush()
httpd.serve_forever()
