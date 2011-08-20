

-- config file -- only use one row...
create table if not exists config(
	results_dir text
	,tmp_dir text
	,base_dir text
);
insert into config 
	(results_dir, tmp_dir, base_dir)
	values
	('/tmp/sos/results', '/tmp', '/tmp/sos');

-- queue runner state (instead of /var/run/sos.pid)
create table if not exists qrstate(
	pid int
	,start_time timestamp default current_timestamp
	,finish_time timestamp
	,current_runid int
	,current_runstate text	
);

-- queue, exitcode is negative for us, positve from shell script
create table if not exists queue (
	run_id text primary key
	,analysis_id text references analyses
	,run_dir text unique
	,run_pushtime timestamp default current_timestamp
	,run_starttime timestamp 
	,run_finishtime timestamp
	,run_exitcode int
	,run_statecode int
	,results blob
	,description text
);

-- analyses
create table if not exists analyses (
	analysis_id text primary key
	,htmlform text	
	,commandstr text
	,description text
);	   
insert into analyses (analysis_id, commandstr, description) values ('wc', 'wc datafile 1>out 2>err', 'counts words in an uploaded file');

-- form key values 
create table if not exists formkv (
	run_id text references queue
	,k text
	,v text
);
-- other state

-- history (not runs, since keep queue)

-- allowed run exit codes

-- users

-- installation and upgrade stuff

-- prime the tables with values
