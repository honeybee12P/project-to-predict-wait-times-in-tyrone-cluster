#!/usr/bin/env python
#client example 
from time import clock, time
import time
import cgi, cgitb
import math, sys, os
import sys
import socket, pickle  #for sockets
host = "10.16.8.112"
port = 8199
usr_data = []
if __debug__:
    import warnings

cgitb.enable()
print "Content-type:text/html\r\n\r\n"
print 
print "<html>"
print "<head>"
print "<title>MetaScheduling</title>"
print "</head>"
print "<body>"
warnings.filterwarnings("ignore",category=RuntimeWarning)

def  clientsocketconn():
#create an INET, STREAMing socket
	#print "this is user data"
	#print usr_data
	try:
    	 s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error:
    	 print 'Failed to create socket'
    	 sys.exit()
     	print 'Socket Created'
	s.connect((host,port))
	if s.connect ==-1:
	   print"error"
	   sys.exit()
	else: 
	 print 'Socket Connected to ' + host + ' on ip ' + host
	data_string = pickle.dumps(usr_data)
	try :
    	 s.send(data_string)
	except socket.error:
    	 print 'Send failed'
    	 sys.exit()
 	print 'Message send successfully'
	reply = s.recv(4096)
	my_array = pickle.loads(reply)
        print "this is recieved from  the server--output"
	for elem in my_array:
  	 print elem
	s.close()

def main():
	queu = 3
	nprocs = 64
	e_rt = 1
	e_rt = (int(e_rt) * 3600)
	"""form = cgi.FieldStorage()  #Get data frmm fields
       #user_jid = 9999#form.getvalue('user_jid')       #9999 Is just a number for indexing within the program.        
	if form.getvalue('queue') == '1':
                queu = '1'
	elif form.getvalue('queue') == '2':
                queu = '2'
        elif form.getvalue('queue') == '3':
                queu = '3'
        elif form.getvalue('queue') == '4':
                queu = '4'
        elif form.getvalue('queue') == '5':
                queu = '5'
        if form.getvalue('nprocs'):
                nprocs = form.getvalue('nprocs')
        else:
                nprocs = '1'
        if form.getvalue('e_rt'):
                e_rt = form.getvalue('e_rt')
                e_rt = (int(e_rt) * 3600)
        else:
                e_rt = '10800'
	"""
        submit = int(time.time())
	usr_data.append(submit)
        usr_data.append(nprocs)
        usr_data.append(e_rt) 
        usr_data.append(queu)
        clientsocketconn() 
	print "</body>"
	print "</html>"
if __name__ == "__main__":# and not "time" in sys.modules:
    main()
