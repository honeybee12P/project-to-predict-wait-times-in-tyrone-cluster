import os #standard python lib
import time #standard python lib
#import run_simulator_parent as run_parent
import run_simulator_client as run_client
from run_simulator_client import RunSimulatorClient
import thread

"""	
def child():
 run_client.main()
#first calls run_simulator_parent.py and then run_simulator_client.py
def parent():
  run_parent.main()
  #print "parent called:	"
  ne = os.fork()
  if ne ==0:
   #print "child called"
   child()  
  else:
   print "parent sleeping"
   time.sleep(10)
"""

if __name__ == "__main__":
   #run_client.main()
   runSimulatorClient = RunSimulatorClient()
   #runSimulatorClient.process()
   thread.start_new_thread(runSimulatorClient.metaScheduler.run, (runSimulatorClient.num_processors,))
   runSimulatorClient.metaScheduler.handle_pred_request()
   
