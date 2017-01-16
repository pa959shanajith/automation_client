#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      sushma.p
#
# Created:
# Copyright:   (c) sushma.p
# Licence:     <your licence>
#-------------------------------------------------------------------------------


import threading
import time

class Me(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        #flag to pause thread
        self.paused = False
        # Explicitly using Lock over RLock since the use of self.paused
        # break reentrancy anyway, and I believe using Lock could allow
        # one thread to pause the worker, while another resumes; haven't
        # checked if Condition imposes additional limitations that would
        # prevent that. In Python 2, use of Lock instead of RLock also
        # boosts performance.
        self.pause_cond = threading.Condition(threading.Lock())
        self.start()
##        self.pause_cond = threading.Condition(threading.Lock())

    def run(self):
##        time.sleep(2)
        print 'runnnnnnnnnnnn'
        for i in range(15):
            with self.pause_cond:
                while self.paused:
                    print '================='
                    self.pause_cond.wait()
                    print 'WAIT Overrrr'

                #thread should do the thing if
                #not paused
            print '+++++++++do the thing',i,'BOOL',self.paused
            time.sleep(2)

    def pause(self):
        self.paused = True
        print 'inside pause'
        # If in sleep, we acquire immediately, otherwise we wait for thread
        # to release condition. In race, worker will still see self.paused
        # and begin waiting until it's set back to False
        self.pause_cond.acquire()

    #should just resume the thread
    def resume(self):
        print 'inside resume'
        self.paused = False
        # Notify so thread will wake after lock released
        self.pause_cond.notify()
        # Now release the lock
        self.pause_cond.release()


def execute():
    import time
    obj=Me()

    obj.pause()
    print 'paused 1'

    time.sleep(3)
    obj.resume()
    time.sleep(8)
    obj.pause()
    print 'paused 2'
    import time
    time.sleep(10)
    obj.resume()

execute()