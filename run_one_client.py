from pymemcache.client import base
from datetime import datetime
import time
import random

client = base.Client(('localhost', 11211))



def acquireBudget(client, amount):
    while (True):
        result, cas = client.gets('budget')
        if result is None:
            result = "1"
        else:
            new_result = int(result) 
            if (new_result <= 0):
                result = "0"
                break
            new_result = new_result - amount
        if client.cas('budget', str(new_result), cas):
            break
    return result

client = base.Client(('localhost', 11211))


t1 = datetime.now()
counter = 0

while (True):
    counter+=1
    if (counter % 1000) == 0:
        print ("Processed 1000 locks ({})".format(counter))
    budget = acquireBudget(client, 1)
    if (int(budget) == 0 ):
        break
t2 = datetime.now()
print ("I took " + str((t2-t1).seconds) + "." + str((t2-t1).microseconds) + " seconds")
print ("We can process {} lock operations per second ".format(counter/ (t2-t1).seconds))


