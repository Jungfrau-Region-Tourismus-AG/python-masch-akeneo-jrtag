# Update to MASCH all 5 minutes
import json
import datetime
from akeneo.akeneo import Akeneo
import sys
sys.path.append("..")

from service.masch import getMaschPull
from service.loadEnv import loadEnv

def maschFlow():
    print ("Masch Flow")
    maschRecords = getMaschPull()
    print(maschRecords)
    if maschRecords['result'] == 'success':
        if len(maschRecords['records']) > 0:
            # Update to Contentdesk
            print("UPDATE to Contentdesk")
        else:
            print("No new records.")
            
def contentdeskFlow():
    print ("Contentdesk Flow")
    targetCon = loadEnv('ziggy')
    target = Akeneo(targetCon["host"], targetCon["clientId"], targetCon["secret"], targetCon["user"], targetCon["passwd"])
    search = '{"labels":[{"operator":"NOT EMPTY","value":""}]}&attributes=labels'
    # maschUpdated
    # maschId
    # maschName
    end_time = datetime.datetime.now()
    start_time = end_time - datetime.timedelta(minutes=5)
    endTimeStr = end_time.strftime("%Y-%m-%dT%H:%M:%S")
    startTimeStr = start_time.strftime("%Y-%m-%dT%H:%M:%S")
    search = '{"maschId":[{"operator":"NOT EMPTY","value":""}],"maschUpdated":[{"operator":"BETWEEN","value":"[' + startTimeStr + ',' + endTimeStr + '"]}]}'
    print(search)
    contentdeskRecords = target.getProductBySearch(search)
    print(contentdeskRecords)
    

def __main__():
    print("STARTING - WORKER")
    maschFlow()
    contentdeskFlow()
    
    
    
    print("END - WORKER")
    
if __name__== "__main__":
    __main__()