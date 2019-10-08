import threading
import time
from ScanGUI import ScannerObj as sco
exitFlag = 0

class wThread (threading.Thread):
   def __init__(self, name):
      threading.Thread.__init__(self)
      self.name = name
   def run(self):
      startTime=time.time()
      print("Starting " + self.name, startTime)
      sco.loadScanners()
      endTime=time.time()
      print("Starting " + self.name, endTime)
      print("elapsed : ", endTime-startTime)









# Create new threads
#thread1 = myThread(1, "Thread-1", 1)
#thread2 = myThread(2, "Thread-2", 2)

# Start new Threads
#thread1.start()
#thread2.start()

#print "Exiting Main Thread"


