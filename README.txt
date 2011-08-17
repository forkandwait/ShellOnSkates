
"Shell-on-skates"  

Synopsis: SOS is a framework for gathering input via forms and running
command line programs with that input via a queue system, all of it in
userspace (typically under public_html/cgi-bin).

SuExec:  To set up suexec for apache is, of course, a royal pain.  I had to
create an "apache" user and group, set up httpd to run as these, keep
these above 500, create a "webbs" group with the same number as webbs
uid, make all my files owned by that group, plus compile apache to use
the apache uid.  