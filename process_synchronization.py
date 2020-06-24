import os
from datetime import datetime
from multiprocessing import Process, Lock, Manager




def info(title):
    print (title)
    print ('module name:' + __name__)
    if hasattr(os, 'getppid'):  
        print ('parent process:' + str( os.getppid()))
    print ('process id:'+ str(os.getpid()))
    

    
def acquireBudget(configDict, configsLock, amount):
    # Use the lock to guard access to budget variable
    configsLock.acquire()
    if (configDict["budget"] >= amount):
        amount_granted = amount
        configDict["budget"] -= amount
    else:
        amount_granted = 0
    configsLock.release()
    return amount_granted



def function1(configsDict, configsLock):
    # Takes care of Symbols 1 .. 50
    info('function f')
    
    counter = 0
    
    # Let's benchmark budget allocation
    t1 = datetime.now()
    while True:
        amount = acquireBudget(configsDict, configsLock, 1)
        #print ("Acquiring Budget " + str(amount))
        counter += 1 
        if (counter % 1000 == 0):
            print ("Processed 1000 locks")
        if amount == 0:
            break

    t2 = datetime.now()
    print ("I took " + str((t2-t1).seconds) + "." + str((t2-t1).microseconds) + " seconds")

    
def function2(configsDict, configsLock):
    # Takes care of Symbols 51 .. 100
    # info('function g')
    counter = 0 


    t1 = datetime.now()
    while True:
        amount = acquireBudget(configsDict, configsLock, 1)
        counter += 1 
        if (counter % 1000 == 0):
            print ("Processed 1000 locks")


        if amount == 0:
            break

    t2 = datetime.now()
    print ("I took " + str((t2-t1).seconds) + "." + str((t2-t1).microseconds) + " seconds")


def function3(configsDict, configsLock):
    # Takes care of Symbols 101 .. 200
    # info('function g')
    counter = 0 
    t1 = datetime.now()
    while True:
        amount = acquireBudget(configsDict, configsLock, 1)
        counter += 1 
        if (counter % 1000 == 0):
            print ("Processed 1000 locks")


        if amount == 0:
            break

    t2 = datetime.now()
    print ("I took " + str((t2-t1).seconds) + "." + str((t2-t1).microseconds) + " seconds")
    print ("We can process {} lock operations per second ".format(100000 / (t2-t1).seconds))



if __name__ == '__main__':
    
    # A manager is necessary for sharing state between threads
    # https://stackoverflow.com/questions/6832554/multiprocessing-how-do-i-share-a-dict-among-multiple-processes
    
    manager = Manager()
    configsDict = manager.dict()
    
    configsLock = Lock()

    # Pre-Set a budget
    configsDict["budget"] = 100000
    
    p1 = Process(target=function1, args=(configsDict, configsLock, ))
    p1.start()
    

    p2 = Process(target=function2, args=(configsDict, configsLock, ))
    p2.start()
    

    p3 = Process(target=function3, args=(configsDict, configsLock, ))
    p3.start()
       
    
    p1.join()
    p2.join()
    p3.join()
