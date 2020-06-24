from pymemcache.client import base
from datetime import datetime
import time
import random

client = base.Client(('localhost', 11211))


def initializeBudget(client):
    client.set('budget', "100000")


result = client.get('budget')

print (type(result))
print ("Old value of budget " + str(result))

initializeBudget(client)
result = client.get('budget')
print ("New value of budget " + str(result))


