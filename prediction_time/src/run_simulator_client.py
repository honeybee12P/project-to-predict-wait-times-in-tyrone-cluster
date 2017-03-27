#! /usr/bin/env python2.4
#calls schedulers/metascheduler.py which only notifies the arrival of the jobs to the predictor and also predicts the ouput of jobs
import sys
if __debug__:
    import warnings
    #warnings.warn("Running in debug mode, this will be slow... try 'python2.4 -O %s'" % sys.argv[0])
from base.event_queue import EventQueue
from base.workload_parser import parse_lines
from base.prototype import _job_inputs_to_jobs
from schedulers.simulator import run_simulator
from schedulers.metaScheduler import runMetaScheduler
from schedulers.metaScheduler import MetaScheduler
#from schedulers.metaScheduler import runMetaScheduler
import time
from schedulers.fcfs_scheduler import FcfsScheduler
from schedulers.conservative_scheduler import ConservativeScheduler
from schedulers.double_conservative_scheduler import DoubleConservativeScheduler
from schedulers.easy_scheduler import EasyBackfillScheduler
from schedulers.double_easy_scheduler import DoubleEasyBackfillScheduler
from schedulers.head_double_easy_scheduler import HeadDoubleEasyScheduler
from schedulers.tail_double_easy_scheduler import TailDoubleEasyScheduler
from schedulers.greedy_easy_scheduler import GreedyEasyBackfillScheduler
from schedulers.easy_plus_plus_scheduler import EasyPlusPlusScheduler
from schedulers.common_dist_easy_plus_plus_scheduler import CommonDistEasyPlusPlusScheduler
from schedulers.alpha_easy_scheduler import AlphaEasyScheduler
from schedulers.shrinking_easy_scheduler import ShrinkingEasyScheduler
from schedulers.easy_sjbf_scheduler import EasySJBFScheduler
from schedulers.reverse_easy_scheduler import ReverseEasyScheduler
from schedulers.perfect_easy_scheduler import PerfectEasyBackfillScheduler
from schedulers.double_perfect_easy_scheduler import DoublePerfectEasyBackfillScheduler
from schedulers.lookahead_easy_scheduler import LookAheadEasyBackFillScheduler
from schedulers.orig_probabilistic_easy_scheduler import OrigProbabilisticEasyScheduler
from schedulers.log_scheduler import LogScheduler
from base.prototype import JobSubmissionEvent, JobTerminationEvent, JobPredictionIsOverEvent  
from base.prototype import ValidatingMachine
from base.event_queue import EventQueue

class RunSimulatorClient(object):

    def __init__(self):
	self.start_time = time.time()
	#input_file = '/home/siddharthsahu/Documents/scheduling/scheduling-virtualenv/prediction/prediction_time/files/tyrone_new_log'
	input_file = '/home/siddharthsahu/Documents/scheduling/scheduling-virtualenv/prediction/history_log_creation/history_log.swf'
	self.num_processors = 800
	l = 1
	input_file = open(input_file)
        if l == 1:
	    #scheduler = EasyBackfillScheduler(num_processors1)
	    self.scheduler = LogScheduler(self.num_processors)
        else:
            print "No such scheduler"
            return
	try:
	  #print "...." 
          jobs = _job_inputs_to_jobs(parse_lines(input_file), self.num_processors)
	  self.metaScheduler = MetaScheduler(jobs, self.num_processors, self.scheduler)
          #runMetaScheduler(num_processors, jobs, scheduler, metaScheduler)
          #print "Num of Processors: ", num_processors1
          #print "Input file: ", input_file
          #print "Scheduler:", type(scheduler)
          #print 'Total scheduled jobs:', scheduler.totalScheduledJobs
        finally:
          if input_file is not sys.stdin:
              input_file.close()  



"""
def main():
   
    start_time = time.time()
    l = 1
    #input_file = '/home/sharath/Desktop/pyss-read-only/src/5K_sample'
    input_file = '/home/sharath/Desktop/pyss-read-only/src/tyrone_new_log'
    num_processors1 = 800
    input_file = open(input_file)
    if l == 1:
	#scheduler = EasyBackfillScheduler(num_processors1)
	scheduler = LogScheduler(num_processors1)
    else:
        print "No such scheduler"
        return  
    try:
        #print "...." 
        runMetaScheduler(
                num_processors = num_processors1 , 
                jobs = _job_inputs_to_jobs(parse_lines(input_file), num_processors1),
  		#print "jobs"
                scheduler = scheduler 
            )
        
        #print "Num of Processors: ", num_processors1
        #print "Input file: ", input_file
        #print "Scheduler:", type(scheduler)
        #print 'Total scheduled jobs:', scheduler.totalScheduledJobs
    finally:
        if input_file is not sys.stdin:
            input_file.close()
    print("Wallclock time: %s seconds" % (time.time() - start_time))

"""
if __name__ == "__main__":# and not "time" in sys.modules:
    try:
        import psyco
        psyco.full()
    except ImportError:
        print "Psyco not available, will run slower (http://psyco.sourceforge.net)"
    main()
