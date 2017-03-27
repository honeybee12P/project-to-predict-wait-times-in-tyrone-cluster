import os
import time
import run_simulator_parent as run_parent
import run_simulator_client as run_client

def child():
 run_client.main()

def parent():
  run_parent.main()
  print "parent called:"
  time.sleep(30)
  ne = os.fork()
  print "child called"
  child()  
 
if __name__ == "__main__":
   parent()
