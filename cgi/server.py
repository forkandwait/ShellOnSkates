#!/usr/bin/env python3

'''*** **************************************************************
    
    PROGRAM: 
    
    DESCRIPTION: Runs a simple cgi server with environment to allow
        for shellonskates.py
    
    PROGRAMMERS:  webb.sprague@ofm.wa.gov    
    
    DATE STARTED: 2011-08-14

    NOTES:  TODO: Add recovery code (try, catch, etc)
    
'/Users/webbs/PROJECTS/SHELL_ON_SKATES/var/SOS.sqlite3'

**********************************************************************************'''

## imports                                                                                                                                        
import argparse
import os
import sys
from http.server import HTTPServer, CGIHTTPRequestHandler

## Handle shell arguments (nifty!)
parser = argparse.ArgumentParser(description='Run SOS server (which runs SOS cgi...).')
parser.add_argument('--port', '-p', type=int, help='Port number for server', default=9999)
parser.add_argument('--db', '-d', type=str, help='Database for CGI')
args = parser.parse_args()
os.environ['SOS_DB']=args.db
PORT = args.port

## set up and fire off cgi server
class Handler(CGIHTTPRequestHandler):
    cgi_directories = ["/"]
httpd = HTTPServer(("", PORT), Handler)
sys.stderr.write("serving at port: %i, home dir: %s\n" %(PORT, os.getcwd()))
sys.stderr.flush()
httpd.serve_forever()
