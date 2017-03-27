#!/usr/bin/env python
import cgi, cgitb
import math, sys, os
from thread import *
import sys
import socket, pickle 
from time import clock, time
import time
import fileinput
HOST = "10.16.8.112"
PORT = 8199
#copied
import sys
if __debug__:
    import warnings
    #warnings.warn("Running in debug mode, this will be slow... try 'python2.4 -O %s'" % sys.argv[0])

from base.workload_parser import parse_lines
from base.prototype import _job_inputs_to_jobs
from schedulers.simulator import run_simulator
from schedulers.metaScheduler import runMetaScheduler
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
class Batch_System:

        # Initialize all the variables
        def __init__(self):
                self.__History_Begin = 1 ; self.__History_End = 180 ; self.__Target_Size = 0 ;self.__TargetJobs_Begin = self.__History_End + 1 #; self.__Target_Size = 0 ; 
                self.JoB_No = [] ; self.User_Req = 0
                self.Max_Nodes = 0 ; self.free_nodes = 0 ; self.__Near_Mid_ShortJobs = 0
                self.__HISTORY_SIZE = self.__History_End - self.__History_Begin
                self.__good_metric_qwt = 0
                self.__history_jobs = [] ; self.__target_jobs = []
                self.__waiting_job_id = [] ; self.__waiting_job_ert = [] ; self.__waiting_job_reqsize = []
                self.__running_job_id = [] ; self.__running_job_reqsize = [] ; self.__running_job_ert = []
                self.__arr_time = {} ; self.__start_time = {} ; self.__wait_time = {} ; self.__real_run_time = {} ; self.__req_size = {} ; self.__est_runtime = {} ; self.__queue_id = {}
                self.__job_rank_reqsize_map = {} ; self.__qsize_map = {} ; self.__free_node_map = {} ; self.__proc_occ_map = {} ; self.__job_rank_ert_map = {} ; self.__job_rank_combo_map = {}
                self.__prev_req_waitq = {} ; self.__prev_ert_waitq = {} ; self.__job_rank_threshold = {}
                self.__metric_list_qwt = [] ; self.__output = []
                self.__reqsize_map = {} ; self.__reqsize_template = [0] ; self.True_positive = 0 ; self.False_positive = 0 ; self.FPos = []
                self.TPos = [] ; self.user_data = [] ; self.req_id = 0
        def log_parser(self):
                #The stuff takes user Input and adds them to the job.txt file   !!!!!
                #print "inpu:",int(inpu[0])
                file_input_log = open("/home/sharath/Desktop/tyrone.swf", 'r')
                lines = file_input_log.readlines()
                for line in lines:
                        job = line.split()
              
                valtopass = int(job[0]) + 1
                
                fil = open("/home/sharath/Desktop/tyrone.swf","a")
 		print "this is inside log parser"
                fil.write(str(int(job[0])+int(1)))
                fil.write("   ")
                fil.write(str(int(self.user_data[0][0]) + int(job[1])))
                fil.write("   ")
                fil.write(str(int(86400)))
                fil.write("   ")
                fil.write(str(int(86400)))
                fil.write("   ")
                fil.write(str(self.user_data[0][1]))
                fil.write("   ")
                fil.write(str(int(job[5])))
                fil.write("   ")
                fil.write(str(int(job[6])))
                fil.write("   ")
                fil.write(str(self.user_data[0][1]))
                fil.write("   ")
                fil.write(str(self.user_data[0][2]))
                fil.write("   ")
                fil.write(str(int(job[9])))
                fil.write("   ")
                fil.write(str(int(1)))
                fil.write("   ")
                fil.write(str(self.user_data[0][3]))
                fil.write("   ")
                fil.write(str(int(-1)))
                fil.write("   ")
                fil.write(str(int(1)))
                fil.write("   ")
                fil.write(str(self.user_data[0][3]))
                fil.write("   ")
                fil.write(str(int(-1)))
                fil.write("   ")
                fil.write(str(int(-1)))
                fil.write("   ")
                fil.write(str(int(-1)))                
                fil.write("\n")
                fil.close()

"""def parent():
   print "before run_simulator_parent"
   os.system("python run_simulator_parent.py")
   time.sleep(10)
   print "after waking up"
  """
def forking_process():
  #call filefinal.py to update the difference between the yesterdays and todays log
  #os.system("python filefinal.py")
  os.system("python run_simulator_parent.py")
  ne=os.fork()
  if ne==0:
   main()
  else:
   #os.system("python run_simulator_parent.py")
   time.sleep(10)
  #sys.exit(0)

def main_part(inpu):
        start_time = time.time()
        system_state = Batch_System()
        system_state.Max_Nodes = system_state.free_nodes = 800 
        system_state.user_data = inpu
        #system_state.convert_logs("tyrone.swf")
        system_state.log_parser()
        end_time = time.time()
        chk = int(end_time-start_time)
        #print "<h2>Time : %s Seconds </h2>" % chk

def  serversocketconn():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print 'Socket created' 
        try:
	 s.bind((HOST, PORT))
        except socket.error , msg:
         print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
         sys.exit()
        print 'Socket bind complete'
        s.listen(10)
        print 'Socket now listening'
       #while 1:#to run it forever
	print "before accept"
        conn, addr = s.accept()
        os.system("sshpass -p praktyr123 ssh secprak@10.16.2.236 'qstat' >outputofqstatnew.txt")
        print 'Connected with ' + addr[0] + ':' + str(addr[1])
        data_string = conn.recv(4096)
        my_array = pickle.loads(data_string)
        print "this is recieved by the server"
        print my_array
        submit1=my_array[0]
        nprocs1=my_array[1]
        e_rt1=my_array[2]
        queu1=my_array[3]
        usr_data = []
        usr_data.append((submit1, nprocs1, e_rt1, queu1))
        print "usr_Data"
        print usr_data
        main_part(usr_data) 
        reply = 'OK.this is server data..'
	#main_part(my_array)
        main1() #calling simulator for target job
        strs=[]
        with open("/home/sharath/Desktop/new-25/newcgi-103/fileappend.txt") as temp_file:
   	  strs = [line.rstrip('\n') for line in temp_file]
        print strs 
        data_reply = pickle.dumps(strs)
        conn.sendall(data_reply)
        conn.close()
        print "this is the end"
        s.close()
        #print "after socket connection"
       

def main1():
    print"inside forked process client"
    l = 1
    input_file = '/home/sharath/Desktop/tyrone.swf'
    num_processors1 = 800
    input_file = open(input_file)

    if l == 1:
       scheduler = EasyBackfillScheduler(num_processors1)
         
    else:
        
        return 
    try:
        #print "...." 
        runMetaScheduler(
                num_processors = num_processors1, 
                jobs = _job_inputs_to_jobs(parse_lines(input_file), num_processors1),
                scheduler = scheduler 
            )
    finally:
        if input_file is not sys.stdin:
            input_file.close()

def main():
    serversocketconn()
    sys.exit(0)
 
if __name__ == "__main__":# and not "time" in sys.modules:
    forking_process()
    print"this is inside main"
    sys.exit(0)
