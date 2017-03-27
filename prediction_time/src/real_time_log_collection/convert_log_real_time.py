import os
import datetime
import calendar
import operator
import time



user_name_id = {}
user_name_id_new = {}

def sort_table(table, col=0):
    return sorted(table, key=operator.itemgetter(col))

def get_month(month_string):
    if month_string == 'Jan':
	return 1
    if month_string == 'Feb':
	return 2
    if month_string == 'Mar':
	return 3
    if month_string == 'Apr':
	return 4
    if month_string == 'May':
	return 5
    if month_string == 'Jun':
	return 6
    if month_string == 'Jul':
	return 7
    if month_string == 'Aug':
	return 8
    if month_string == 'Sep':
	return 9
    if month_string == 'Oct':
	return 10
    if month_string == 'Nov':
	return 11
    if month_string == 'Dec':
	return 12

def get_timestamp(job_data_elem, param): 
    year = int(job_data_elem[job_data_elem.index(param)+6])
    temp_month = job_data_elem[job_data_elem.index(param)+3]
    month = int(get_month(temp_month))
    day = int(job_data_elem[job_data_elem.index(param)+4])
    hour = int(job_data_elem[job_data_elem.index(param)+5].split(':')[0])
    minute = int(job_data_elem[job_data_elem.index(param)+5].split(':')[1])
    sec = int(job_data_elem[job_data_elem.index(param)+5].split(':')[2])
    temp_time = datetime.datetime(year, month, day, hour, minute, sec)
    return calendar.timegm(temp_time.utctimetuple())


def do_conversion():
    #print "In do conversion"
    #nothing			    #job_id qstat-f: line 1
    job_start_time = {}             #'start_time': line 117
    job_queued_time = {}		#'qtime': line 107
    job_user_name = {}		#'Job_Owner': line 3
    job_owner = {}
    job_exec_name = {}		#
    job_queue_name = {}		#'queue': line 9 
    job_exit_status = {}		#
    job_cpu_time = {}		#
    job_wall_time = {}		#'resource_used.walltime': not required
    job_mem_used = {}		#'resource_used.mem': line 5
    job_vmem_used = {}		#'resource_used.vmem': line 6
    user_id_map = {}		#
    unique_user_id = 1		#
    exec_id_map = {}		#
    unique_exec_id = 1		#
    queue_id_map = {}		#
    queue_id_map['idqueue'] = 0	
    queue_id_map['qp32'] = 1	
    queue_id_map['qp64'] = 2	
    queue_id_map['qp128'] = 3	
    queue_id_map['qp256'] = 4
    #queue_id_map['batch'] = 5 

    path = '/home/siddharthsahu/Documents/scheduling/scheduling-virtualenv/prediction/prediction_time/src/real_time_log_collection/qstat_f'

    present_time = calendar.timegm(datetime.datetime.now().utctimetuple())
    job_data = []

    with open(path,'r') as file_data:
        data = file_data.read()
        job_data = data.split('\n\n')
        del job_data[-1]

    all_jobs = []            
    for elem in job_data:
      try:
        current_job = []
        job_data_elem = elem.split()
        job_queue = job_data_elem[job_data_elem.index('queue')+2]
        if job_queue == 'batch' or job_queue == 'idqueue':
	    continue
        job_id = job_data_elem[job_data_elem.index('Id:')+1].split('.')[0]
        job_state = job_data_elem[job_data_elem.index('job_state')+2]
        queue_time = get_timestamp(job_data_elem, 'qtime')
	print "\nqtime = ",queue_time
        #user_id for Deployment
        job_owner[job_id] = job_data_elem[job_data_elem.index('Job_Owner')+2].split('@')[0]
	#print "check output ",job_queue[2:], " ",job_id
        no_cores = int(job_queue[2:])
        if job_state == 'Q':
            start_time = 0
	    job_mem = 0
	    job_vmem = 0
        else:
            start_time = get_timestamp(job_data_elem, 'start_time')
            job_mem = int(job_data_elem[job_data_elem.index('resources_used.mem')+2][:-2])
            job_vmem = int(job_data_elem[job_data_elem.index('resources_used.vmem')+2][:-2])
  
        current_job.append(job_id)
        current_job.append(queue_time)
        if job_state == 'Q':
            current_job.append(int(present_time - queue_time))
        else:
            current_job.append(int(start_time - queue_time))
        if job_state == 'Q':
	    current_job.append(0)
        else:
	    current_job.append(-1)
        user_id = 0
        if job_owner[job_id] in user_id_map.keys():
            user_id =  user_id_map[job_owner[job_id]]
        else:
            user_id_map[job_owner[job_id]] = unique_user_id
            unique_user_id += 1
            user_id =  user_id_map[job_owner[job_id]]
        current_job.append(no_cores)
        current_job.append(0)
        current_job.append(job_mem)
        current_job.append(no_cores)
        current_job.append(24*3600)
        current_job.append(-1)	#req mem
        current_job.append(-1)	#status 
        #current_job.append(-1)  #user_id
        #user_id for Deployment
        current_job.append(user_id)
        current_job.append(-1)
        current_job.append(-1)
        current_job.append(-1)
        current_job.append(-1)
        current_job.append(-1)
        current_job.append(-1)

        all_jobs.append(current_job)

      except:
	pass    #to handle tyrone logging and formating errors which occured multiple times

    sort_table(all_jobs, col=1)
    print "In real log"
    ofile = open("/home/siddharthsahu/Documents/scheduling/scheduling-virtualenv/prediction/prediction_time/src/real_time_log_collection/real_time_log_2.swf",'w')
    for item in all_jobs:
        for val in item:
	    print >>ofile, val, ' ',
        print >>ofile, ""

    ofile.close()
    
    user_id_file = open("/home/siddharthsahu/Documents/scheduling/scheduling-virtualenv/prediction/history_log_creation/user_id_file",'a+')
    lines =  user_id_file.readlines()
    for each in lines:
	line_split = each.split()
        user_name_id.update({str(line_split[0]):int(line_split[1])})
    
    for key, value in user_id_map.iteritems():
        
        if key in user_name_id.keys():
           #print "user already in common file\t",key
           continue
        else:
           user_name_id_new.update({str(key):int(value)})
 	   
        
    
    for key, value in user_name_id_new.iteritems():
    	user_id_file.write(str(key))
        #print "Coming from real time\t",key
    	user_id_file.write("\t")
    	user_id_file.write(str(value))
    	user_id_file.write("\n")
    user_id_file.close()
if __name__ == "__main__":
    do_conversion()
    	

