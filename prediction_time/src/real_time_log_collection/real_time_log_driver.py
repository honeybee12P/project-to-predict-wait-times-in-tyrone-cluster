import sys
import os
import paramiko
from convert_log_real_time import do_conversion

def read_real_logs():
    try:
        if 1:
            # Connect to remote host
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect('tyrone-cluster.serc.iisc.ernet.in', username='secvin', password='test123')

            # Setup sftp connection and transmit this script
	    """
            sftp = client.open_sftp()
            sftp.put(__file__, './test.bash')
            sftp.close()
	    """
            # Run the transmitted script remotely without args and show its output.
            # SSHClient.exec_command() returns the tuple (stdin,stdout,stderr)
	    """
	    # code to run 'qstat' command only
            stdout = client.exec_command('qstat')[1]
	    target_qstat = './qstat'
	    stdout_qstat = stdout.read()
	    target_qstat = open(target_qstat, 'w')
	    target_qstat.write(stdout_qstat)
	    target_qstat.close()
	    """
	    #print "In driver"
	    target_qstat_f = '/home/siddharthsahu/Documents/scheduling/scheduling-virtualenv/prediction/prediction_time/src/real_time_log_collection/qstat_f'
	    target_qstat_f = open(target_qstat_f, 'w')
	    stdout = client.exec_command('qstat -f')[1]
            output_data = stdout.read()
	    target_qstat_f.write(output_data)
	    target_qstat_f.close()
            client.close()
	    do_conversion()
            #sys.exit(0)
    except IndexError:
        pass

if __name__ == '__main__':

    # No cmd-line args provided, run script normally
    read_real_logs()
