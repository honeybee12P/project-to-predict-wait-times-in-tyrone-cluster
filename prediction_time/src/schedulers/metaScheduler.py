#!/usr/bin/env python2.4

from prediction_time.src.base.prototype import JobSubmissionEvent, JobTerminationEvent, JobPredictionIsOverEvent 
from prediction_time.src.base.prototype import ValidatingMachine
from prediction_time.src.base.workload_parser import JobInput, parse_lines
from prediction_time.src.base.prototype import _job_inputs_to_jobs, _job_input_to_job
from prediction_time.src.base.event_queue import EventQueue
from common import CpuSnapshot, list_print
#from schedulers1.metaScheduler import *
from easy_plus_plus_scheduler import EasyPlusPlusScheduler
from shrinking_easy_scheduler import ShrinkingEasyScheduler
from copy import deepcopy
from prediction_time.src.base.prototype import JobStartEvent

from simulator import Simulator
import time
import thread
import Maingain as Mainval
import est_runtime_assump as assumpt
EnabledWaitPred = True
EnabledRunPred = True
#start_time = time.time()
if EnabledRunPred:
	from prediction_time.src.predictors.run import RuntimePrediction
	RunPredictor = RuntimePrediction.Batch_System	 
        

if EnabledWaitPred:
	from prediction_time.src.predictors.wait import QueueWaitingTime
	WaitPredictor = QueueWaitingTime.Batch_System

import math
import sys
import random
from prediction_time.src.real_time_log_collection.real_time_log_driver import read_real_logs
from prediction_time.src.daily_log_update.daily_log_driver import fetch_daily_logs

class MetaScheduler(object):
    """
    This class is the common interface between the User, Predictor and Site Scheduler
    Tasks:
     - Accept job inputs from user
     - Obtain predictions
     - Submit jobs to scheduler
     - Provide feedback (if necessary) to user and predictor
    """

    def __init__(self, jobs, num_processors, scheduler):
        
        self.num_processors = num_processors
        self.jobs = jobs
        self.do_pred = 0
        #print "inside init of metascheduler"
	#print "jobs",jobs
        #print len(self.jobs)
        
        self.terminated_jobs=[]
        self.scheduler = scheduler
        self.time_of_last_job_submission = 0
        self.event_queue = EventQueue()
       
	#with open('/home/siddharthsahu/Documents/scheduling/scheduling-virtualenv/prediction/prediction_time/files/tyrone_new_log') as f:
	with open('/home/siddharthsahu/Documents/scheduling/scheduling-virtualenv/prediction/history_log_creation/history_log.swf') as f:
           a = sum(1 for _ in f)
        #print "value of history:",a
        self.historySetSize = a-1
        
        #self.historySetSize = 0
         
        self.currentSubmitCount = 0

	if EnabledWaitPred:
            self.waitTimePredictor = WaitPredictor()
	else:
            self.waitTimePredictor = None

        if EnabledRunPred:
            self.runTimePredictor = RunPredictor()
	    
        else:
            self.runTimePredictor = None

        self.machine = ValidatingMachine(num_processors=num_processors, event_queue=self.event_queue, wait_predictor=self.waitTimePredictor, run_predictor = self.runTimePredictor, scheduler = self.scheduler)

        self.event_queue.add_handler(JobSubmissionEvent, self.handle_submission_event)
        self.event_queue.add_handler(JobTerminationEvent, self.handle_termination_event)
        
        if isinstance(scheduler, EasyPlusPlusScheduler) or isinstance(scheduler, ShrinkingEasyScheduler):
            self.event_queue.add_handler(JobPredictionIsOverEvent, self.handle_prediction_event)
        
        countSubmissions = 0    
        for job in self.jobs:
            countSubmissions += 1
            self.event_queue.add_event( JobSubmissionEvent(job.submit_time, job) )     
        #print '** Added', countSubmissions, 'job submission events to event queue **'
        self.queueSimulator = Simulator(jobs, num_processors, scheduler, self.event_queue, self.machine, )

    def modify_job_attributes(self, event, newRequestSize, actual_runtime, actual_ert):
	    #print "modify_job_attributes"
	    oldRunTime = event.job.actual_run_time
	    event.job.num_required_processors = newRequestSize
	    event.job.user_estimated_run_time = actual_ert
	    event.job.predicted_run_time = actual_ert
	    if actual_runtime == 0:
		event.job.actual_run_time = actual_ert
	    else:
                event.job.actual_run_time = actual_runtime
           

    def change_job_attributes(self, event, newRequestSize,actual_ert):
	    #print "change job attributes"
            oldRunTime = event.job.actual_run_time
	    event.job.num_required_processors = newRequestSize
	    #event.job.user_estimated_run_time = actual_ert
	    #event.job.predicted_run_time = actual_ert
	    

    def decision_metrics(self, event,queuedJobs,runningJobIDs,allrunningjobevents,jobtarrun):
        #print "inside decision metrics"
        #print "event:",event
	
       
        #queuedJobIDs = [j.id for j in self.event_queue.QueuedJobs]
        #runningJobIDs = [j.id for j in self.event_queue.RunningJobs]
        #queuedJobIDs.append(event.job.id)
       
        originalRequestSize = event.job.num_required_processors
        waitPredictions = {}
        responsePredictions = {}
	waittime_list = []
        run_list = []
        wait_list = []
        submittime = []
        #terminateval = []
	ifcounter = 0
        if EnabledRunPred:
            run_list.append(jobtarrun)
            submittime.append(event.job.submit_time)
            waitPredictions = self.waitTimePredictor.get_prediction(event.job)
            wait_list.append(waitPredictions)
            pred_run,runid = self.runTimePredictor.get_predictiondelay(event.job)
            
            
            if(len(runid) > 1):
             
             for i in runid:
              ifcounter += 1
              
              for obj in allrunningjobevents:
             	 if obj.id == i in runningJobIDs:
                       terminateval = obj
              
              runningJobIDs.remove(i)
            
              relevantRunningObjs = []
              
	      for obj in allrunningjobevents:
             	 if obj.id in runningJobIDs:
	             relevantRunningObjs.append(obj)
             
              self.runTimePredictor.notify_job_termination_event(terminateval)
              
               
              if EnabledWaitPred:
                    
                    self.waitTimePredictor.notify_arrival_event(event.job, queuedJobs, relevantRunningObjs) 
                    self.runTimePredictor.notify_arrival_event(event.job, queuedJobs, relevantRunningObjs)
                    #if self.currentSubmitCount > self.historySetSize:
                    #print "afterifcondition:"
                    #print "counter:",ifcounter
                    waitPredictions = self.waitTimePredictor.get_prediction(event.job)#to obtain waittime prediction for all running jobs
                    wait_list.append(waitPredictions)
                    #print "wait_prediction:",waitPredictions
                    RunPredictions  = self.runTimePredictor.get_actprediction(event.job)#to obtain runtime prediction for all running jobs
                    #print "run_prediction:",RunPredictions
                    run_list.append(RunPredictions)
                    submittime.append(event.job.submit_time+RunPredictions)
                 
                    runningJobIDs.append(i)
                
             delay = [];decision_list = []
             if( len(wait_list) != [] and len(wait_list) != []):
              l = submittime[0]
              for ru in range(len(run_list)):
                delay.append(abs(l-submittime[ru]))
              
              for k in range(len(wait_list)):
                decision_list.append(wait_list[k]+run_list[k]+delay[k])
              #print "eventjob:",event.job.id
              cjob = event.job.id
              runid.insert(0,cjob)
              inmade = decision_list.index(min(decision_list))
              
              return runid,cjob,runid[inmade],inmade,delay
             else:
              empty = []
              return empty,event.job.id,event.job.id,1,empty
            else:
              empty = []
              return empty,event.job.id,event.job.id,1,empty
#study from here

    def handle_submission_event(self, event):
        assert isinstance(event, JobSubmissionEvent)
        self.currentSubmitCount += 1
        queuedJobs = self.event_queue.QueuedJobs[:]
        queuedJobs.append(event.job)
        originalRequestSize = event.job.num_required_processors
        waitPredictions = {}
        responsePredictions = {}
	waittime_list = []
	

        if EnabledRunPred:
            self.runTimePredictor.notify_arrival_event(event.job, queuedJobs, self.event_queue.RunningJobs) 
	    
                
            #if self.currentSubmitCount > self.historySetSize:     #in true means no waiting required? but why?
               
                #processor_list,estimated_runtims,histjobs,wt_jobs,ru_jobs,jnu,subtm,prore,usid,rtime,wtime,reqt,qid,my_id,myest,mypoinval,myranpro = self.runTimePredictor.get_prediction(event.job)#CALL FOR RUNTIME PREDICTION job molding
                #print "hello",''
            
	        
            if EnabledWaitPred:
              self.waitTimePredictor.notify_arrival_event(event.job, queuedJobs, self.event_queue.RunningJobs) 
              """
              if self.currentSubmitCount > self.historySetSize:
	       
               if( len(processor_list) > 1):  #processor_list: is the list of required processors for jobs by same user which are in history jobs list. For more explaination refer '__processor_lists' in RuntimePrediction.py
               
                for val in processor_list:
                    self.change_job_attributes(event,val,myest)
                    
                  
                    waitPredictions[val] = self.waitTimePredictor.get_prediction(event.job)		# Getting the wait time prediction lists for different processor
                       
                    
                    waittime_list.append(waitPredictions[val])
               
              
                final_proc = Mainval.Pick_value(processor_list,waittime_list,estimated_runtims) #best processor selection based on gain value
                bestRequestSize = final_proc
                #estimated time calculations
                actual_runtime, actual_ert = assumpt.ert_runtime_list_generator(final_proc,histjobs,wt_jobs,ru_jobs,jnu,subtm,prore,usid,rtime,wtime,reqt,qid,my_id)

                print "Job no:",event.job.id,
		print " Actual Wait time:",event.job.actual_wait_time,
                #print "Runtime_rangeset:",myranpro[0],'\n'
                print " Predicted Wait time:",waittime_list[0],' '
                #print "Runtime_pointval:",mypoinval[0],'\n'
                #print "Job Molding:",'\n'
                #print "requested_processor:",processor_list[0],'\n'
                #print "Processor_Selected:",final_proc,'\n'
                #print "Estimated_runtime:",actual_ert,'\n'
                runningJobIDs = [j.id for j in self.event_queue.RunningJobs]
                allrunningjobevents = self.event_queue.RunningJobs
                #call for delayed submission
                id_list,jobcrid,changid,index_val,delay_list = self.decision_metrics(event,queuedJobs,runningJobIDs,allrunningjobevents,mypoinval[0])
            
		
                #if(jobcrid == changid):
                #
                #  print "Delayed Submission:",'\n'
                #  print "Delay:",0,'\n'
                #  print "Submit_time:",event.job.submit_time,'\n'
		#
                #else:
                #
                # print "Delayed Submission:",'\n'
                # print "Delay:",min(delay_list),'\n'
                # sub = event.job.submit_time + min(delay_list)
                # print "Submit_time:",sub,'\n'
                
		self.modify_job_attributes(event, bestRequestSize, actual_runtime, actual_ert)
                self.waitTimePredictor.notify_arrival_event(event.job, queuedJobs, self.event_queue.RunningJobs)
                self.runTimePredictor.notify_arrival_event(event.job, queuedJobs, self.event_queue.RunningJobs)
	       
	       waitPred = self.waitTimePredictor.get_prediction(event.job)
	       print "Job no:",event.job.id,
	       print "\t",event.job.actual_wait_time,
	       print "\t",waitPred,' '
	      """
        self.queueSimulator.handle_submission_event(event)

    def handle_termination_event(self, event):
        assert isinstance(event, JobTerminationEvent)
        #print 'Term event:', event
        #self.scheduler.cpu_snapshot.printCpuSlices()
        self.queueSimulator.handle_termination_event(event)
        #queuedJobIDs = [j.id for j in self.event_queue.QueuedJobs]
        #runningJobIDs = [j.id for j in self.event_queue.RunningJobs]

        if EnabledWaitPred:
            self.waitTimePredictor.notify_job_termination_event(event.job, self.event_queue.QueuedJobs, self.event_queue.RunningJobs)
	if EnabledRunPred:
            self.runTimePredictor.notify_job_termination_event(event.job)

    def handle_prediction_event(self, event):
        assert isinstance(event, JobPredictionIsOverEvent)
        self.queueSimulator.handle_prediction_event(event)
      
    def run(self, num_processors):
        while not self.event_queue.is_empty:
        #    print_simulator_stats(self.queueSimulator)
            self.event_queue.advance()
        self.do_pred = 1
	#time.sleep(5)
        loop = 1
	while loop == 1:
	    fetch_daily_logs()
            daily_file = '/home/siddharthsahu/Documents/scheduling/scheduling-virtualenv/prediction/prediction_time/src/daily_log_update/tyrone_daily.swf'	
	    #daily_file = '/home/siddharthsahu/Documents/scheduling/scheduling-virtualenv/sample_logs/log_daily'
	    daily_file = open(daily_file)
	    if daily_file.closed:
	      print "File status: daily file is closed"
	    else:
	      print "File status: daily file is open"
	    today_jobs = _job_inputs_to_jobs(parse_lines(daily_file), num_processors)

	    runQueuedJobIDs = [j.id for j in self.event_queue.QueuedJobs]
	    runRunningJobIDs = [j.id for j in self.event_queue.RunningJobs]

	    #print "runQueuedJobIDs = ", runQueuedJobIDs
	    #print "runRunningJobIDs = ", runRunningJobIDs
	    #print "self machine jobs=", self.machine.jobs

	    today_count = 0
	    for today_job in today_jobs:
	      if today_job.actual_run_time != 0:
		today_job.start_to_run_at_time = today_job.submit_time + today_job.actual_wait_time
	      if today_job.id in runQueuedJobIDs:
	        self.event_queue.add_event( JobStartEvent(today_job.submit_time + today_job.actual_wait_time, today_job) )   #since job is already queued, hence can be in daily log file only because it started running
	        #add job start event
	      #elif today_job in self.event_queue.RunningJobs:
	      elif today_job.id in runRunningJobIDs:
	        self.event_queue.add_event( JobTerminationEvent(today_job.submit_time + today_job.actual_wait_time + today_job.actual_run_time, today_job) )
	        #add job termination event
	      else:
	        self.event_queue.add_event( JobSubmissionEvent(today_job.submit_time, today_job) )
	    while not self.event_queue.is_empty:	#changing state as these jobs are also considered
	        self.event_queue.advance()
		#print_simulator_stats(self.queueSimulator)
	    time.sleep(86400)
	#time.sleep(1000)
         

    def handle_pred_request(self):		#sid
      loop = 1
      while loop == 1:
        #while(self.do_pred == 0):	#DO-IT when new prediction is requested set this to 1
	#  time.sleep(1)
        req_file = '/home/siddharthsahu/Documents/scheduling/scheduling-virtualenv/prediction/prediction_time/files/req_file'
	#req_file = '/home/siddharthsahu/Documents/scheduling/scheduling-virtualenv/sample_logs/log_req'
        try:
	    req_file = open(req_file)
	    #req_file.readline()
	    req_job = _job_input_to_job(JobInput(req_file.readline()), 800)
        finally:
	    if req_file is not sys.stdin:
                req_file.close()

	read_real_logs()
	temp_file = '/home/siddharthsahu/Documents/scheduling/scheduling-virtualenv/prediction/prediction_time/src/real_time_log_collection/real_time_log_2.swf'
	#temp_file = '/home/siddharthsahu/Documents/scheduling/scheduling-virtualenv/sample_logs/log_real'
	temp_file = open(temp_file)
	#Imp note: temp_jobs is a generator. Hence normal list funtions like len() won't work
	temp_jobs = _job_inputs_to_jobs(parse_lines(temp_file), 800) #pass no of processors as argument
	
	self.temp_currentSubmitCount = self.currentSubmitCount  #updated at handleSubmissionEvent
	#temp_countSubmissions = self.countSubmissions	
	
	#temp variable deepcopied of original variables
	
	self.temp_scheduler = deepcopy(self.scheduler)

	self.temp_event_queue = EventQueue()
	self.temp_event_queue.events_heap = deepcopy(self.event_queue._events_heap)
	#temp_event_queue._handlers = deepcopy(self.event_queue._handlers) this is giving error. Hence can't copy whole event_queue at once
	self.temp_event_queue._latest_handled_timestamp = deepcopy(self.event_queue._latest_handled_timestamp)
	self.temp_event_queue.RunningJobs = deepcopy(self.event_queue.RunningJobs)
	self.temp_event_queue.QueuedJobs = deepcopy(self.event_queue.QueuedJobs)
	self.temp_event_queue.add_handler(JobSubmissionEvent, self.temp_handle_submission_event)
	self.temp_event_queue.add_handler(JobTerminationEvent, self.temp_handle_termination_event)
	
	self.temp_waitTimePredictor = deepcopy(self.waitTimePredictor)
	self.temp_runTimePredictor = deepcopy(self.runTimePredictor)
	
	self.temp_machine = ValidatingMachine(800, event_queue=self.temp_event_queue, wait_predictor=self.temp_waitTimePredictor, run_predictor = self.temp_runTimePredictor, scheduler = self.temp_scheduler)
	self.temp_machine.jobs = self.machine.jobs
	

	self.temp_queueSimulator = Simulator(self.jobs, 800, self.temp_scheduler, self.temp_event_queue, self.temp_machine, )
	self.temp_queueSimulator.terminated_jobs = self.queueSimulator.terminated_jobs
	self.temp_queueSimulator.time_of_last_job_submission = self.queueSimulator.time_of_last_job_submission

	#remove finished waiting and running jobs from temp_event_queue. As We don't know finish time of jobs waiting or running at day begining but finished now, we need to drop them

	#because job list is generator and for other problems we have to remove jobs through below arduous method

	remove_jobs_id = []
	remove_jobs = []

	queuedJobID = [j.id for j in self.event_queue.QueuedJobs]
	runningJobID = [j.id for j in self.event_queue.RunningJobs]


	temp_jobs_list = []
	temp_jobs_id = []
	temp_shift_jobs = [] #jobs which move from queued to running
	temp_shift_jobs_id = []
	dont_remove_ids = []
	#print "Validation: queuedJobID=", queuedJobID, " runningJobID=", runningJobID
	#print "Validation: Imp: temp_jobs=", len(temp_jobs)
	for job in temp_jobs:
	    print "Validation: real_job_id=", job.id, " actual_run_time=", job.actual_run_time
	    if (job.id in queuedJobID and job.actual_run_time == 0) or (job.id in runningJobID and job.actual_run_time == -1):	#if job is still in same queue, no action
		dont_remove_ids.append(job.id)
	    else:
		if job.id in queuedJobID and job.actual_run_time == -1:	#remove from queued, if moved to running
		    temp_shift_jobs.append(job)
		    temp_shift_jobs_id.append(job.id)
		else:
	    	    temp_jobs_list.append(job)	#list of jobs to be added; either to waiting or running queue
	    	    temp_jobs_id.append(job.id)
	

	print "temp_shift_jobs:",temp_shift_jobs
	print "temp_jobs:",temp_jobs_id
	print "QueuedJobs:",self.event_queue.QueuedJobs
	print "RunningJObs:",self.event_queue.RunningJobs

	for job in self.event_queue.QueuedJobs:	#queued jobs which have been finished
	    if job.id not in temp_jobs_id and job.id not in temp_shift_jobs_id and job.id not in dont_remove_ids:		
		remove_jobs_id.append(job.id)
		
	for job in self.event_queue.RunningJobs:	#running jobs which have been finished
	    if job.id not in temp_jobs_id and job.id not in dont_remove_ids:
		remove_jobs_id.append(job.id)

	for job in self.temp_event_queue.QueuedJobs:
	    if job.id in remove_jobs_id:
		remove_jobs.append(job)

	for job in self.temp_event_queue.RunningJobs:
	    if job.id in remove_jobs_id:
		remove_jobs.append(job)
	    
	for job in remove_jobs:
	    if job in self.temp_event_queue.QueuedJobs:
		print "removed Job from Queued Jobs", job.id,"\n"
	        self.temp_event_queue.QueuedJobs.remove(job)
	    else:
		print "removed Job from Running Jobs", job.id,"\n"
		self.temp_event_queue.RunningJobs.remove(job)
	
	for job in temp_jobs_list:
	    #Validation
	    if job.id == 10499:
		print "Validation: 10499: job.actual_run_time=", job.actual_run_time
	    self.temp_event_queue.add_event(JobSubmissionEvent(job.submit_time,job))

	for job in temp_shift_jobs:
	    self.temp_event_queue.add_event(JobStartEvent(job.submit_time+job.actual_wait_time, job))
	
	while not self.temp_event_queue.is_empty:
	    print_simulator_stats(self.temp_queueSimulator)
	    self.temp_event_queue.advance()
	
	"""
	#Waittime prediction without considering realtime update
        self.runTimePredictor.notify_arrival_event(req_job, self.event_queue.QueuedJobs[:], self.event_queue.RunningJobs)
        self.waitTimePredictor.notify_arrival_event(req_job, self.event_queue.QueuedJobs[:], self.event_queue.RunningJobs)
        waitPred = self.waitTimePredictor.get_prediction(req_job)
	"""

	#Waittime prediction considering realtime update
	pred_queuedJobs = self.temp_event_queue.QueuedJobs[:] #For Deployment
	pred_queuedJobs.append(req_job)		#For Deployment
	self.temp_runTimePredictor.notify_arrival_event(req_job, pred_queuedJobs, self.temp_event_queue.RunningJobs)
        self.temp_waitTimePredictor.notify_arrival_event(req_job, pred_queuedJobs, self.temp_event_queue.RunningJobs)
	print "\nQueued Jobs: ", self.temp_event_queue.QueuedJobs
	print "\nRunning Jobs: ", self.temp_event_queue.RunningJobs
        waitPred = int(self.temp_waitTimePredictor.get_prediction(req_job))
	print "Validation: Prediction=", waitPred

	out_file = '/home/siddharthsahu/Documents/scheduling/scheduling-virtualenv/prediction/prediction_time/files/predictions.txt'
	out_file = open(out_file, 'w')
        out_file.write(str(req_job.id))
        out_file.write("\t")
        out_file.write(str(req_job.actual_wait_time))
        out_file.write("\t")
	out_file.write(str(waitPred))
	out_file.close()
	self.do_pred = 0
        #print "Job no:",req_job.id,
        #print "\t",req_job.actual_wait_time,
        #print "\t",waitPred,
	#print "\t",req_job.user_estimated_run_time,
	#print "\t",req_job.actual_run_time,' '
	loop = loop + 1
    
    def temp_handle_submission_event(self, event):
	    assert isinstance(event, JobSubmissionEvent)
            self.temp_currentSubmitCount += 1
            queuedJobs = self.temp_event_queue.QueuedJobs[:]
            queuedJobs.append(event.job)
            originalRequestSize = event.job.num_required_processors
            waitPredictions = {}
            responsePredictions = {}
	    waittime_list = []
	

            if EnabledRunPred:
                self.temp_runTimePredictor.notify_arrival_event(event.job, queuedJobs, self.temp_event_queue.RunningJobs)     
                if EnabledWaitPred:
                  self.temp_waitTimePredictor.notify_arrival_event(event.job, queuedJobs, self.temp_event_queue.RunningJobs) 
            self.temp_queueSimulator.handle_submission_event(event)


    def temp_handle_termination_event(self, event):
	    assert isinstance(event, JobTerminationEvent)
            self.temp_queueSimulator.handle_termination_event(event)
            #queuedJobIDs = [j.id for j in self.event_queue.QueuedJobs]
            #runningJobIDs = [j.id for j in self.event_queue.RunningJobs]

            if EnabledWaitPred:
                self.temp_waitTimePredictor.notify_job_termination_event(event.job, self.temp_event_queue.QueuedJobs, self.temp_event_queue.RunningJobs)
	    if EnabledRunPred:
                self.temp_runTimePredictor.notify_job_termination_event(event.job)

def runMetaScheduler(num_processors, jobs, scheduler, metaScheduler):
    try:
      thread.start_new_thread(metaScheduler.handle_pred_request, ())
    except:
      print "Error: unable to start thread",''
    metaScheduler.run(num_processors)						#sid if parent thread{ MS.run() sleep(for a day)} if child thread{wait for web interface; update recent log and get prediction} #problem is parent updated data structures available in child
    print_simulator_stats(metaScheduler.queueSimulator)
    return metaScheduler

def print_simulator_stats(simulator):
    simulator.scheduler.cpu_snapshot._restore_old_slices()
    # simulator.scheduler.cpu_snapshot.printCpuSlices()
    #print_statistics(simulator.terminated_jobs, simulator.time_of_last_job_submission)

# increasing order 
by_finish_time_sort_key   = (
    lambda job : job.finish_time
)

# decreasing order   
#sort by: bounded slow down == max(1, (float(wait_time + run_time)/ max(run_time, 10))) 
by_bounded_slow_down_sort_key = (
    lambda job : -max(1, (float(job.start_to_run_at_time - job.submit_time + job.actual_run_time)/max(job.actual_run_time, 10)))
)

    
def print_statistics(jobs, time_of_last_job_submission):
    assert jobs is not None, "Input file is probably empty."
    maxwt = [];max_runt = []
    nwait_sum = nrun_sum = 0
    nwait_sum1 = nrun_sum1 = 0
    nwait_sum2 = nrun_sum2 = 0
    nwait_sum3 = nrun_sum3 = 0
    nwait_sum4 = nrun_sum4 = 0
    nwait_sum5 = nrun_sum5 = 0
    nwait_sum6 = nrun_sum6 = 0
    sum_waits     = 0
    sum_run_times = 0
    sum_slowdowns           = 0.0
    sum_bounded_slowdowns   = 0.0
    sum_estimated_slowdowns = 0.0
    sum_tail_slowdowns      = 0.0
    target_start_id = 10000
    coun = coun1 = coun2 = coun3 = coun4 = coun5 = coun6 = 0
    counter = tmp_counter = tail_counter = 0
    
    size = len(jobs)
    precent_of_size = int(size / 100)
    
    for job in sorted(jobs, key=by_finish_time_sort_key):
        tmp_counter += 1
        if job.id < target_start_id:
            continue  
            

        if job.user_estimated_run_time == 1 and job.num_required_processors == 1: # ignore tiny jobs for the statistics
            size -= 1
            precent_of_size = int(size / 100)
            continue
        
        if size >= 100 and tmp_counter <= precent_of_size:
            continue
        
        if job.finish_time > time_of_last_job_submission:
            break 
        
        counter += 1
        
        wait_time = float(job.start_to_run_at_time - job.submit_time)
        run_time  = float(job.actual_run_time)
        estimated_run_time = float(job.user_estimated_run_time)

        maxwt.append(wait_time)
        max_runt.append(run_time)
        if( len(maxwt) != 0):
         sum_waits += wait_time
         sum_run_times += run_time
         sum_slowdowns += float(wait_time + run_time) / run_time
         sum_bounded_slowdowns   += max(1, (float(wait_time + run_time)/ max(run_time, 10))) 
         sum_estimated_slowdowns += float(wait_time + run_time) / estimated_run_time
         if(abs(job.start_to_run_at_time-job.finish_time) > 0 and abs(job.start_to_run_at_time-job.finish_time) <= 3600):
            nwait_sum += wait_time
            nrun_sum += run_time
            coun += 1
         elif(abs(job.start_to_run_at_time-job.finish_time) > 3600 and abs(job.start_to_run_at_time-job.finish_time) <= 10800):
            nwait_sum1 += wait_time
            nrun_sum1 += run_time
            coun1 += 1
         elif(abs(job.start_to_run_at_time-job.finish_time) > 10800 and abs(job.start_to_run_at_time-job.finish_time) <= 21600):
            nwait_sum2 += wait_time
            nrun_sum2 += run_time
            coun2 += 1
         elif(abs(job.start_to_run_at_time-job.finish_time) > 21600 and abs(job.start_to_run_at_time-job.finish_time) <= 32400):
            nwait_sum3 += wait_time
            nrun_sum3 += run_time
            coun3 += 1
         elif(abs(job.start_to_run_at_time-job.finish_time) > 32400 and abs(job.start_to_run_at_time-job.finish_time) <= 43200):
            nwait_sum4 += wait_time
            nrun_sum4 += run_time
            coun4 += 1
         elif(abs(job.start_to_run_at_time-job.finish_time) > 43200 and abs(job.start_to_run_at_time-job.finish_time) <= 86400):
            nwait_sum5 += wait_time
            nrun_sum5 += run_time
            coun5 += 1
         elif(abs(job.start_to_run_at_time-job.finish_time) > 86400):
            nwait_sum6 += wait_time
            nrun_sum6 += run_time
            coun6 += 1
        if max(1, (float(wait_time + run_time)/ max(run_time, 10))) >= 3:
            tail_counter += 1
            sum_tail_slowdowns += max(1, (float(wait_time + run_time)/ max(run_time, 10)))
            
    sum_percentile_tail_slowdowns = 0.0
    percentile_counter = counter
    
    for job in sorted(jobs, key=by_bounded_slow_down_sort_key):
        wait_time = float(job.start_to_run_at_time - job.submit_time)
        run_time  = float(job.actual_run_time)
        sum_percentile_tail_slowdowns += float(wait_time + run_time) / run_time
        percentile_counter -= 1 # decreamenting the counter 
        if percentile_counter < (0.9 * counter):
            break
        
        
        
    print
    if( len(maxwt) != 0):
     print "STATISTICS: "
    
     print "Wait (Tw) [minutes]: ", float(sum_waits) / (60 * max(counter, 1))

     print "Response time (Tw+Tr) [minutes]: ", float(sum_waits + sum_run_times) / (60 * max(counter, 1))
    
     print "min_qwt,max_qwt:",min(maxwt),max(maxwt)
     print "min_responsetime,max_responsetime:",min(max_runt),max(max_runt)

     print "Slowdown (Tw+Tr) / Tr: ", sum_slowdowns / max(counter, 1)

     print "Bounded slowdown max(1, (Tw+Tr) / max(10, Tr): ", sum_bounded_slowdowns / max(counter, 1)
    
     print "Estimated slowdown (Tw+Tr) / Te: ", sum_estimated_slowdowns / max(counter, 1)
 
     print "Tail slowdown (if bounded_sld >= 3): ", sum_tail_slowdowns / max(tail_counter, 1)
     print "   Number of jobs in the tail: ", tail_counter

     print "Tail Percentile (the top 10% sld): ", sum_percentile_tail_slowdowns / max(counter - percentile_counter + 1, 1)    
    
     print "Total Number of jobs: ", size
    
     print "Number of jobs used to calculate statistics: ", counter


     print "ranges <1(wait,run,counter):",nwait_sum,nrun_sum,coun
     print "ranges 1-3(wait,run,counter):",nwait_sum1,nrun_sum1,coun1
     print "ranges 3-6(wait,run,counter):",nwait_sum2,nrun_sum2,coun2
     print "ranges 6-9(wait,run,counter):",nwait_sum3,nrun_sum3,coun3
     print "ranges 9-12(wait,run,counter):",nwait_sum4,nrun_sum4,coun4
     print "ranges 12-1day(wait,run,counter):",nwait_sum5,nrun_sum5,coun5
     print "ranges >1day(wait,run,counter):",nwait_sum6,nrun_sum6,coun6
     print "--- seconds ---:",time.time() - start_time
     print
     
