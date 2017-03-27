# from __future__ import unicode_literals
from __future__ import division
#from numpy.ma import append
from django.template import Template, Context
import re, collections
import math
import thread
import string
from collections import Counter
from prediction_time.models import contact
from random import randint
import time
from django.core.context_processors import csrf
from django.utils import timezone
from datetime import datetime
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from prediction_time.src import main_run
from prediction_time.src import run_simulator_client
#from django.db.models import Avg
from django.template import Context, Template
import ast
#from notification.models import Notification
#from django.db.models.signals import post_save
#from notifications import notify
from django.db.models import Sum
import urllib
import random
from django.template import Template
import json
import pickle
from django.contrib import messages
#import textblob
#from textblob import TextBlob
#import language_check
from django.template import Library, Template
#from django.utils import simplejson
from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.utils.safestring import mark_safe
from prediction.urls import getSimulatorObject
import datetime
import calendar
#from textblob._text import Context
from xlwt import Workbook
import xlrd
import xlwt
from xlutils.copy import copy
r = 1 
#request.session.get('row') = row
def interface(request):

    return render(request, 'submit.html')
def contributors(request):
    
    return render(request, 'contributors.html')

def contactus(request):
    
    return render(request, 'contactus.html')
def howitworks(request):
    
    return render(request, 'howitworks.html')

def contact_us(request):
    
    if 'cname' in request.GET and request.GET['cname']:
        name = request.GET['cname']
        
    if 'cemail' in request.GET and request.GET['cemail']:
        email = request.GET['cemail']
    if 'cmessage' in request.GET and request.GET['cmessage']:
        message = request.GET['cmessage']
    #b = contact(contact_name = name, contact_email = email, contact_message = message)
    #b.save()
    #return render(request, 'contactus.html')
    #HttpResponse(email)
    #"""
    """
    wb = Workbook()
    sheet = wb.add_sheet('Contact Us')
    sheet.write(0,0,"Name")
    sheet.write(0,1,"Email ID")
    sheet.write(0,2,"Message")
    
    sheet.col(0).width = 5000
    sheet.col(1).width = 5000
    sheet.col(2).width = 10000
    
    
    #r = request.session.get('row') + 1 
    #request.session.get('row') = r 
    global r
    
    sheet.write(r,0,name)
        
    sheet.write(r,1,email)
        
    sheet.write(r,2,message)
    r = r + 1  
    #row = row + 1
   
    wb.save('Contactus.xls')
    """
    rb = xlrd.open_workbook('Contactus.xls',formatting_info=True)
    r_sheet = rb.sheet_by_index(0) 
    r = r_sheet.nrows
    wb = copy(rb) 
    sheet = wb.get_sheet(0) 
    sheet.write(r,0,name)
    sheet.write(r,1,email)
    sheet.write(r,2,message)
    wb.save('Contactus.xls')
    return HttpResponseRedirect("/interface/#section3")

def get_data_from_user(request):
    user_id = 0
    queue_id = 0
    #if 'queue' in request.GET and request.GET['queue']:
        #queue = request.GET['queue']
        #queue = int(q)
    #if 'processors' in request.GET and request.GET['processors']:
        #processors = request.GET['processors']
    #if 'ert' in request.GET and request.GET['ert']:
        #ert = request.GET['ert']
    if 'userid' in request.GET and request.GET['userid']:
        userid = request.GET['userid']
    #return HttpResponse(userid)
    if 'q' in request.GET and request.GET['q']:
        processors = request.GET['q']

    if processors == "qp32":
       p = int(32)
       queue_id = 1
    elif processors == "qp64":
       p = int(64)
       queue_id = 2
    elif processors == "qp128":
       p = int(128)
       queue_id = 3
    else:
       p = int(256)
       queue_id = 4
    #username = userid.split('@')[0]
    username = str(userid)
    #return HttpResponse(username)
    present = datetime.datetime.now()
    present_utc = calendar.timegm(present.utctimetuple())
    user_name_id = {}
    user_id_file = open("/home/siddharthsahu/Documents/scheduling/scheduling-virtualenv/prediction/history_log_creation/user_id_file",'a+')
    lines =  user_id_file.readlines()
    for each in lines:
	line_split = each.split()
        user_name_id.update({str(line_split[0]):int(line_split[1])})
    print "User Name id\t",user_name_id
    if str(username) in user_name_id.keys():
	user_id = user_name_id[str(username)]
    else:
	user_name_key = max(user_name_id, key=user_name_id.get)
        user_id = int(user_name_id[str(user_name_key)]) + 1
        #new_user_id = user_id
        #user_name_id.update({str(username):int(user_id)})
        #user_id_file.close()
        #user_id_file_1 = open("/home/kruthika/Documents/tyrone_log/user_id_file",'a')
        #if username not in user_name_id.keys():  
        user_id_file.write(str(username))
        user_id_file.write("\t")
        user_id_file.write(str(user_id))
        user_id_file.write("\n")
    
    #hist =open('/home/kruthika/Documents/scheduling/scheduling-virtualenv/prediction/prediction_time/src/history.txt','r')
    #if queue == "qp32":
       #q = 32
    #elif queue == "qp64":
       #q = 64
    #elif queue == "qp128":
       #q = 128
    #elif queue == "qp256":
       #q = 256
    #elif queue == "idqueue":
       #q = 32

    #last_line = file('/home/kruthika/Desktop/src/tyrone_new.swf', "r").readlines()[-1]
    last_line = file('/home/siddharthsahu/Documents/scheduling/scheduling-virtualenv/prediction/history_log_creation/history_log.swf',"r").readlines()[-1]
    last = last_line.split()
    target_jobid = int(last[0]) + 1
    #target = open('/home/kruthika/Documents/scheduling/scheduling-virtualenv/prediction/prediction_time/src/req_file','w')
    target = open('/home/siddharthsahu/Documents/scheduling/scheduling-virtualenv/prediction/prediction_time/files/req_file','w')
    target.write(str(int(target_jobid)+10000))
    target.write("\t")
    #target.write(str(last[1]))
    target.write(str(present_utc))
    target.write("\t")
    target.write(str(last[2]))
    target.write("\t")
    #target.write(str(last[3]))
    target.write("0")
    target.write("\t")
    target.write(str(p))
    target.write("\t")
    #target.write("-1")
    target.write(str(last[5]))
    target.write("\t")
    #target.write("-1")
    target.write(str(last[6]))
    target.write("\t")
    target.write(str(p))
    target.write("\t")
    #target.write(str(ert))
    #target.write("200")
    target.write(str(last[8]))
    target.write("\t")
    #target.write("-1")
    target.write(str(last[9]))
    target.write("\t")
    #target.write("-1")
    target.write(str(last[10]))
    target.write("\t")
    #target.write("-1")
    #target.write(str(last[11]))
    target.write(str(user_id))
    #print "user id for secvin\t",user_id
    target.write("\t")
    #target.write("-1")
    target.write(str(last[12]))
    target.write("\t")
    #target.write("-1")
    target.write(str(last[13]))
    
    
    target.write("\t")
    #target.write("-1")
    #target.write(str(last[14]))
    target.write(str(queue_id))
    target.write("\t")
    #target.write("-1")
    target.write(str(last[15]))
    target.write("\t")
    #target.write("-1")
    target.write(str(last[16]))
    
    target.write("\t")
    #target.write("-1")
    target.write(str(last[17]))
    target.write("\n")
    #target.write("\t")
    target.close()

    ##main_run.run_client.main()
    #runSimulatorClient = run_simulator_client.RunSimulatorClient()
    #thread.start_new_thread(runSimulatorClient.metaScheduler.run, (runSimulatorClient.num_processors,))
    #runSimulatorClient.metaScheduler.handle_pred_request()
    runSimulatorClient = getSimulatorObject()
    runSimulatorClient.metaScheduler.handle_pred_request()
    
    #present_utc
    daily_jobs = []    
    daily_wait_times = []
    tyrone_daily = open('/home/siddharthsahu/Documents/scheduling/scheduling-virtualenv/prediction/prediction_time/src/daily_log_update/tyrone_daily.swf','r')
    daily_lines = tyrone_daily.readlines()
    for each in daily_lines:
	daily_jobs.append(each)
    #print "Daily Jobs list\t",daily_jobs
    print "Present UTC\t", present_utc
    for job in daily_jobs:
        each = job.split()
	if int(each[1]) > (present_utc-1) and int(each[1]) < (present_utc+1):
              daily_wait_times.append(each[2])
    print "Daily_wait_times\t",daily_wait_times
    res = open('/home/siddharthsahu/Documents/scheduling/scheduling-virtualenv/prediction/prediction_time/files/predictions.txt','r')
    res = res.read()
    r = res.split()
    #print "prediction split\t",r
    results = 1
    #pred_time = time.strftime("%H h: %M m : %S s", time.gmtime(int(r[2])))
    minute, second = divmod(int(r[2]), 60)
    hour, minute = divmod(minute, 60)
    pred_time = str(hour)+" h : "+str(minute)+" m : "+str(second)+" s"
    return render(request, 'submit.html',
                  {'results':results,'id': r[0],'ActualTime':r[1],'PredictedTime':pred_time,'queue':processors})




