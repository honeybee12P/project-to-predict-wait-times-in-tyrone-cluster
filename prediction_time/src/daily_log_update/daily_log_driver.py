#import sys
#import os
import datetime
from datetime import timedelta
import paramiko
from convert_log_daily import daily_log_conversion

def fetch_daily_logs():
    try:
	now = datetime.datetime.now() - timedelta(days=1)

	#debug_code starts
        todaydate = now.strftime('%Y-%m-%d %H:%M:%S')
        todaydate_list = todaydate.split()[0].split('-')
	filename = str(todaydate_list[0]) + str(todaydate_list[1]) + str(todaydate_list[2])
	#filename = str(now.year) + str(now.month) + str(now.day)
	#debug_code ends
	
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect('tyrone-cluster.serc.iisc.ernet.in', username='secvin', password='test123')

	print filename

	sftp = client.open_sftp()
	sftp.get('/var/spool/torque/server_logs/'+filename,'/home/siddharthsahu/Documents/scheduling/scheduling-virtualenv/prediction/prediction_time/src/daily_log_update/server_logs/'+filename)
	sftp.get('/var/spool/torque/sched_logs/'+filename,'/home/siddharthsahu/Documents/scheduling/scheduling-virtualenv/prediction/prediction_time/src/daily_log_update/sched_logs/'+filename)
	sftp.close()
	print "completed daily log driver"
    except IndexError:
	pass

    daily_log_conversion()
	

if __name__ == '__main__':
    fetch_daily_logs()	