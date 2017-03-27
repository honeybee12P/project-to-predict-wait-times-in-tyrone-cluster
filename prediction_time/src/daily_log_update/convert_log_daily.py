import os
import datetime
from datetime import timedelta
import calendar
import operator
import time as timeLib    #since there is also a variable named time

#user_id for Deployment
#user_id_file = open("/home/kruthika/Documents/tyrone_log/user_id_file",'a')


user_name_id = {}
user_name_id_new = {}

def sort_table(table, col=0):
    return sorted(table, key=operator.itemgetter(col))

def daily_log_conversion():

    present_time = timeLib.time()
    job_start_time = {}
    job_queued_time = {}
    job_user_name = {}
    job_exec_name = {}
    job_queue_name = {}
    job_exit_status = {}
    job_cpu_time = {}
    job_wall_time = {}
    job_mem_used = {}
    job_vmem_used = {}
    user_id_map = {}
    unique_user_id = 1
    exec_id_map = {}
    unique_exec_id = 1
    queue_id_map = {}
    queue_id_map['idqueue'] = 0
    queue_id_map['qp32'] = 1
    queue_id_map['qp64'] = 2
    queue_id_map['qp128'] = 3
    queue_id_map['qp256'] = 4
    #queue_id_map['batch'] = 5 

    temp_filename = datetime.datetime.now() - timedelta(days=1)
    

    #debug_code starts
    todaydate = temp_filename.strftime('%Y-%m-%d %H:%M:%S')
    todaydate_list = todaydate.split()[0].split('-')
    filename = str(todaydate_list[0]) + str(todaydate_list[1]) + str(todaydate_list[2])
    #filename = str(temp_filename.year) + str(temp_filename.month) + str(temp_filename.day)
    #debug_code ends

    path = '/home/siddharthsahu/Documents/scheduling/scheduling-virtualenv/prediction/prediction_time/src/daily_log_update/sched_logs/'+filename  # remove the trailing '\'


    now = datetime.datetime.now() - timedelta(days=1)

    write_jobs = set()

    sched_data = {}
    if os.path.isfile(path):
	with open(path, 'r') as my_file:
	    sched_data[int(filename)] = my_file.readlines()
    else:
	print "\nSched doesn't have file"

    """	
    for dir_entry in os.listdir(path):
        dir_entry_path = os.path.join(path, dir_entry)
        if os.path.isfile(dir_entry_path):
            with open(dir_entry_path, 'r') as my_file:
                sched_data[dir_entry] = my_file.readlines()
    print 'Read', len(sched_data), 'sched logs'
    """

    path = '/home/siddharthsahu/Documents/scheduling/scheduling-virtualenv/prediction/prediction_time/src/daily_log_update/server_logs/'+filename  # remove the trailing '\'

    server_data = {}
    if os.path.isfile(path):
        with open(path, 'r') as my_file:
	    server_data[int(filename)] = my_file.readlines()
    else:
	print "\nServer doesn't has file"

    """
    for dir_entry in os.listdir(path):
        dir_entry_path = os.path.join(path, dir_entry)
        if os.path.isfile(dir_entry_path):
            with open(dir_entry_path, 'r') as my_file:
                server_data[dir_entry] = my_file.readlines()
    print 'Read', len(server_data), 'server logs'
    """

    for sched_file_id in sched_data:
        sched_file_data = sched_data[sched_file_id]
        #print "inside sched file"
        #print sched_file_id
        #print sched_file_data
        #print 'Processing file', sched_file_id
        for line in sched_file_data:
            #print line
            sline = line.split()
            if sline[-1] == 'Run':
                #print sline
                #job_id = sline
                temp = sline[2]
                job_id = int((temp.split('.')[0]).split(';')[2])
                #print temp, job_id
                date = sline[0]
                time = sline[1].split(';')[0]
                #print job_id, date, time
                sdate = date.split('/')
                month = int(sdate[0])
                day = int(sdate[1])
                year = int(sdate[2])
                stime = ((time.split(';'))[0]).split(':')
                hour = int(stime[0])
                mins = int(stime[1])
                sec = int(stime[2])
    	        if year == now.year and month == now.month and day == now.day:
		    write_jobs.add(job_id)		
                #print job_id, month, day, year, hour, mins, sec
                #print type(hour)
                startTime = datetime.datetime(year, month, day, hour, mins, sec)
                #print job_id, startTime.ctime()
                timeStamp = calendar.timegm(startTime.utctimetuple())
                #print timeStamp
                #print startTime.time()
                job_start_time[job_id] = timeStamp
            
    print 'No. of job start times read:', len(job_start_time.keys()) 
    '''
     08/30/2012 10:18:44;0008;PBS_Server;Job;9590.tyrone-cluster;Job Queued at request of csdsuben@tyrone-cluster, owner = csdsuben@tyrone-cluster, job name = zrph6, queue = batch
    ['08/30/2012', '10:18:44;0008;PBS_Server;Job;9590.tyrone-cluster;Job', 'Queued', 'at', 'request', 'of', 'csdsuben@tyrone-cluster,', 'owner', '=', 'csdsuben@tyrone-cluster,', 'job', 'name', '=', 'zrph6,', 'queue', '=', 'batch']
    08/30/2012 10:19:37;0010;PBS_Server;Job;9497.tyrone-cluster;Exit_status=0 resources_used.cput=729:39:16 resources_used.mem=2482064kb resources_used.vmem=16582964kb resources_used.walltime=23:32:24
    ['8/30/2012', '10:19:37;0010;PBS_Server;Job;9497.tyrone-cluster;Exit_status=0', 'resources_used.cput=729:39:16', 'resources_used.mem=2482064kb', 'resources_used.vmem=16582964kb', 'resources_used.walltime=23:32:24']
'''
    job_queued_date = {}
    deleted_jobs_list = []

    for server_file_id in server_data:
        server_file_data = server_data[server_file_id]
        #print 'Processing file', server_file_id
        for line in server_file_data:
            #print line
            sline = line.split()
            if len(sline) > 2 and sline[2] == 'Queued':
                #print 'here'
                # get job id
                job_id = int((sline[1].split(';'))[4].split('.')[0])
                date = sline[0]
                time = sline[1].split(';')[0]
                sdate = date.split('/')
                month = int(sdate[0])
                day = int(sdate[1])
                year = int(sdate[2])
                stime = ((time.split(';'))[0]).split(':')
                hour = int(stime[0])
                mins = int(stime[1])
                sec = int(stime[2])
    	        if day == now.day and month == now.month and year == now.year:
    		    write_jobs.add(job_id)
                #job_queued_date_time[job_id] = [date, time]
            
                queuedTime = datetime.datetime(year, month, day, hour, mins, sec)
                timeStamp = calendar.timegm(queuedTime.utctimetuple())

                job_queued_time[job_id] = timeStamp
                job_user_name[job_id] = sline[6].split('@')[0]
                job_exec_name[job_id] = sline[13][:-1]
                job_queue_name[job_id] = sline[-1]
                #print "intialvalue:",job_id, job_queued_time[job_id], job_user_name[job_id], job_exec_name[job_id], job_queue_name[job_id]

            if len(sline) > 2 and sline[2].startswith('resources_used'):
                #print 'here'
                job_id = int((sline[1].split(';'))[4].split('.')[0])
                date = sline[0]
                time = sline[1].split(';')[0]
                sdate = date.split('/')
                month = int(sdate[0])
                day = int(sdate[1])
                year = int(sdate[2])
                stime = ((time.split(';'))[0]).split(':')
                hour = int(stime[0])
                mins = int(stime[1])
                sec = int(stime[2])
    	        if day == now.day and month == now.month and year == now.year:
    		    write_jobs.add(job_id)
                finishTime = datetime.datetime(year, month, day, hour, mins, sec)
                timeStamp = calendar.timegm(finishTime.utctimetuple())
                job_exit_status[job_id] = int(sline[1].split(';')[-1].split('=')[1])
                cput = sline[2].split('=')[1]
                cputseconds = int(cput.split(':')[0])*3600 + int(cput.split(':')[1])*60 + int(cput.split(':')[2])
                used_memory = int((sline[3].split('=')[1][:-2]))
                vmem = int((sline[4].split('=')[1][:-2]))
                wallt = sline[5].split('=')[1]
                walltseconds = int(wallt.split(':')[0])*3600 + int(wallt.split(':')[1])*60 + int(wallt.split(':')[2])
		if walltseconds == 0:
		    walltseconds = 1

                job_cpu_time[job_id] = cputseconds
                job_wall_time[job_id] = walltseconds
                job_mem_used[job_id] = used_memory
                job_vmem_used[job_id] = vmem
          
            if len(sline) > 2 and sline[2] == 'deleted':
                job_id = int((sline[1].split(';'))[4].split('.')[0])
                deleted_jobs_list.append(job_id)
    print 'No. of job queued times read:', len(job_queued_time.keys())           
    #print job_queued_time

    temp_count = 0
    for key in job_start_time:
      if key not in job_wall_time:
        temp_count += 1
        print key
    print "temp_count = ",temp_count,''

    anomalies = 0
    both_Exist = 0
    for key in job_queued_time:
        if key in job_start_time:
            both_Exist += 1
            #print job_queued_time[key], job_start_time[key]
        
            if job_start_time[key] <job_queued_time[key]:
                #print  job_start_time[key]-job_queued_time[key]
	        print "Anomaly job: ", key
                anomalies += 1

    #print anomalies, 'out of', both_Exist


    swf_log = []
    job_unique_id = 1
    date_boundary = datetime.datetime.today() - datetime.timedelta(seconds=86400*30)
    utc_date_boundary = calendar.timegm(date_boundary.utctimetuple())
    utc_current_time =  calendar.timegm(datetime.datetime.today().utctimetuple())
    #today_datetime = datetime.datetime(datetime.datetime.today().year, datetime.datetime.today().month, datetime.datetime.today().day, 0, 0, 0)
    #utc_current_time = calendar.timegm(today_datetime.utctimetuple())
    queued_list_file = open("/home/siddharthsahu/Documents/scheduling/scheduling-virtualenv/prediction/prediction_time/src/daily_log_update/tyrone_queued_list.log", 'w')
    target_jobs_count = 0
    #print "This is key"
    #print key  
    #print "This is key"
    for key in job_queued_time.keys():
        job_id = key
    
        target_job = False
        try:
            if not job_id in job_start_time and job_id in job_queued_time and not job_id in deleted_jobs_list and utc_date_boundary <= job_queued_time[job_id]:
                print >>queued_list_file, job_id
                print job_id, job_user_name[job_id], job_queue_name[job_id]
                target_job = True
                target_jobs_count += 1
                # Each target job has been waiting till the current time. So we can write the wait time as at least current time - submit time and the queue. This is true when daily log creations is almost same as daily log files fetching (server and sched logs)
                # states for the prediction algorithm won't be affected
            wait_time = 0
            if target_job: 
		wait_time = utc_current_time - job_queued_time[job_id]
                #wait_time = utc_current_time - job_queued_time[job_id] + 3600 # just to ensure it doesn't interfere with the discerete event simulator
            else:
                wait_time = job_start_time[job_id] - job_queued_time[job_id]
                if job_start_time[key] <job_queued_time[key]:
                    continue

            current_job = []

            current_job.append(job_id)	    
            current_job.append(job_queued_time[job_id])
            current_job.append(wait_time)

            if target_job: 
                current_job.append(0)
            else:
    	        if key not in job_wall_time:		#sid jobs which are in still running
                  if job_start_time[key] + 10*24*60*60 < present_time:	#jobs running more that 10 days, drop these
                    raise ValueError("These jobs are running more than 10 days")
                  current_job.append(-1)
                else:
                  current_job.append(job_wall_time[job_id])
        
            nodes = 1
            #if job_queue_name[job_id] == 'qp128' or job_queue_name[job_id] == 'qp256' : 
            #    nodes = 4
            avg_cpu_time = 0

            if target_job or key not in job_wall_time:
                job_cpu_time[job_id] = 0
                job_mem_used[job_id] = 0
                job_exit_status[job_id] = 99999

            if job_queue_name[job_id] == 'qp256': 
                nodes = 256
                avg_cpu_time = job_cpu_time[job_id]/256
            if job_queue_name[job_id] == 'qp128': 
                nodes = 128
                avg_cpu_time = job_cpu_time[job_id]/128
            if job_queue_name[job_id] == 'qp64': 
                nodes = 64
                avg_cpu_time = job_cpu_time[job_id]/64
            if job_queue_name[job_id] == 'qp32': 
                nodes = 32
                avg_cpu_time = job_cpu_time[job_id]/32
            if job_queue_name[job_id] == 'idqueue': 
                nodes = 32
                avg_cpu_time = job_cpu_time[job_id]/32
            
            current_job.append(nodes)
            current_job.append(avg_cpu_time)
            current_job.append(job_mem_used[job_id])
            current_job.append(nodes)
            #print "current_job:",current_job//print correctly the first 8 values
            requested_time = 24*3600
            if job_queue_name[job_id] == 'idqueue': 
                requested_time = 2*3600
            requested_mem = -1

            status = job_exit_status[job_id]
            user_id = 0
            if job_user_name[job_id] in user_id_map.keys():
                user_id =  user_id_map[job_user_name[job_id]]
            else:
                user_id_map[job_user_name[job_id]] = unique_user_id
                unique_user_id += 1
                user_id =  user_id_map[job_user_name[job_id]]

            exec_id = 0
            if job_exec_name[job_id] in exec_id_map.keys():
                exec_id =  exec_id_map[job_exec_name[job_id]]
            else:
                exec_id_map[job_exec_name[job_id]] = unique_exec_id
                unique_exec_id += 1
                exec_id =  exec_id_map[job_exec_name[job_id]]

            group_id = -1
            partition_id = -1
            preceeding_job = -1
            think_time = -1

            current_job.append(requested_time)
            current_job.append(requested_mem)
            current_job.append(status)
            current_job.append(user_id)
        
            current_job.append(group_id)
            current_job.append(exec_id)
            current_job.append(queue_id_map[job_queue_name[job_id]])
            #print "current_job:",current_job//print correctly the first 15 values
            current_job.append(partition_id)
        
            current_job.append(preceeding_job)
            current_job.append(think_time)
            #print "current_job:",current_job
            #current_job.append(job_id)
            #current_job.append(job_user_name[job_id])
            #current_job.append(job_exec_name[job_id])
            #current_job[0] = job_unique_id
            #job_unique_id += 1 #line number here
            swf_log.append(current_job)
	    #print "swf_log =", swf_log
            #, job_user_name[job_id], job_exec_name[job_id], job_queue_name[job_id], job_cpu_time[job_id], job_wall_time[job_id], job_mem_used[job_id], job_vmem_used[job_id], job_start_time[job_id], wait_time, 'cpus:', job_cpu_time[job_id]/job_wall_time[job_id]
        
        except Exception as ex:
    	    print "exception key = ",key," ", type(ex).__name__," ",ex.args, " "        
	    pass
    
    #new code begins
    #For jobs which starts running or finished only today. Earlier event were in previous dates
    start_keys = set(job_start_time) - set(job_queued_time)
    end_keys = set(job_wall_time) - set(job_start_time) - set(job_queued_time)
    history_path = "/home/siddharthsahu/Documents/scheduling/scheduling-virtualenv/prediction/history_log_creation/history_log.swf"
    hist_data = ""
    hist_jobs = {}
    with open(history_path, 'r') as hist_file:
	    hist_data = hist_file.readlines()

    for line in hist_data:
	temp_job = line.split()
        temp_job_id = int(temp_job[0])
	if temp_job_id in start_keys or temp_job_id in end_keys:
	    hist_jobs[int(temp_job[0])] = temp_job
    
    temp_swf_log = []
    for temp_job_id in hist_jobs.keys():
	print hist_jobs[temp_job_id]

    #print "hist_jobs are: ", hist_jobs.keys()
    
    print "Division"
    for temp_job_id in hist_jobs.keys():
	current_job = []
	temp_job = hist_jobs[temp_job_id]
	current_job.append(int(temp_job_id))
	current_job.append(int(temp_job[1]))

	if temp_job_id in start_keys:
	    temp_wait_time = job_start_time[temp_job_id] - int(temp_job[1])	#job has started but not finished
	else:
	    temp_wait_time = int(temp_job[2])
	current_job.append(int(temp_wait_time))

	if temp_job_id in job_wall_time.keys():
	    temp_run_time = job_wall_time[temp_job_id]
	else:
	    temp_run_time = -1
	current_job.append(int(temp_run_time))

	"""
	if temp_job_id in start_keys:
	    temp_run_time = -1
	else:
	    temp_run_time = job_wall_time[temp_job_id]
	current_job.append(int(temp_run_time))
	"""

	current_job.append(int(temp_job[4]))
	if temp_job_id in start_keys:
	    temp_cpu_used = 0
	else:
	    temp_cpu_used = job_cpu_time[temp_job_id]/int(temp_job[4])
	current_job.append(int(temp_cpu_used))

	if temp_job_id in start_keys:
	    temp_mem_used = 0
	else:
	    temp_mem_used = job_mem_used[temp_job_id]
	current_job.append(int(temp_mem_used))

	current_job.append(int(temp_job[7]))
	current_job.append(int(temp_job[8]))
	current_job.append(int(temp_job[9]))
	current_job.append(int(temp_job[10]))
	current_job.append(int(temp_job[11]))
	current_job.append(int(temp_job[12]))
	current_job.append(int(temp_job[13]))
	current_job.append(int(temp_job[14]))
	current_job.append(int(temp_job[15]))
	current_job.append(int(temp_job[16]))
	current_job.append(int(temp_job[17]))

	swf_log.append(current_job)


    print "start_keys= ",start_keys 
    print "end_keys= ",end_keys
    
    #new code ends


    sort_table(swf_log,col=1)

    print "\n Write_jobs : ",write_jobs
    ofile = open("/home/siddharthsahu/Documents/scheduling/scheduling-virtualenv/prediction/prediction_time/src/daily_log_update/tyrone_daily.swf", 'w')
    for item in swf_log:
      if item[0] in write_jobs:
        for val in item:
    	    #print val
            print >>ofile, val,' ',
	    #print val
        print >>ofile,""

    ofile.close()
    
    user_id_file = open("/home/siddharthsahu/Documents/scheduling/scheduling-virtualenv/prediction/history_log_creation/user_id_file",'a+')
    lines =  user_id_file.readlines()
    for each in lines:
	line_split = each.split()
        user_name_id.update({str(line_split[0]):int(line_split[1])})
   
    
    for key, value in user_id_map.iteritems():
        
        if key in user_name_id.keys():
           continue
        else:
           user_name_id_new.update({str(key):int(value)})
 	   
       
    for key, value in user_name_id_new.iteritems():
    	user_id_file.write(str(key))
        print "Coming from daily log\t",key
    	user_id_file.write("\t")
    	user_id_file.write(str(value))
    	user_id_file.write("\n")
    #user_id for Deployment
    
    user_id_file.close()
    data_structures=[
    job_start_time,
    job_queued_time,
    job_user_name,
    job_exec_name,
    job_queue_name,

    job_exit_status,
    job_cpu_time,
    job_wall_time,
    job_mem_used,
    job_vmem_used,

    user_id_map,
    exec_id_map,
    queue_id_map]

    data_structures_names=[
    'job_start_time',
    'job_queued_time',
    'job_user_name',
    'job_exec_name',
    'job_queue_name',

    'job_exit_status',
    'job_cpu_time',
    'job_wall_time',
    'job_mem_used',
    'job_vmem_used',

    'user_id_map',
    'exec_id_map',
    'queue_id_map']


    for ids in range(len(data_structures)):
        print data_structures_names[ids], len(data_structures[ids].keys())

    print 'Target jobs:', target_jobs_count
    print "completed convert log daily"

#daily_log_conversion()
