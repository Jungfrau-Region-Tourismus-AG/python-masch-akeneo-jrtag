# Update to MASCH all 5 minutes
import json
import datetime
from akeneo.akeneo import Akeneo
import sys
sys.path.append("..")

from service.masch import getMaschPull
from service.loadEnv import loadEnv
import service.debug as debug

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
    startDay = end_time - datetime.timedelta(days=1)
    endDayStr = end_time.strftime("%Y-%m-%d")
    startDayStr = startDay.strftime("%Y-%m-%d")
    search = '{"maschId":[{"operator":"NOT EMPTY","value":""}],"maschUpdated":[{"operator":"BETWEEN","value":["' + startDayStr + '","' + endDayStr + '"]}]}'
    print(search)
    contentdeskRecords = target.getProductBySearch(search)
    debug.addToFileFull("worker", "ziggy", "export", "maschId", "extractProducts", contentdeskRecords)
    recentRecords = []
    for record in contentdeskRecords:
        # string to datetime
        maschUpdatedStr = record['values']['maschUpdated'][0]['data']
        print("maschUpdatedStr")
        print(maschUpdatedStr)
        maschUpdated = datetime.datetime.fromisoformat(maschUpdatedStr)
        maschUpdated = maschUpdated.strftime('%Y-%m-%d %H:%M:%S')
        #maschUpdated = datetime.datetime.strptime(maschUpdatedStr, '%Y-%m-%d %H:%M:%S')
        #maschUpdated = datetime.datetime.strptime(record['values']['maschUpdated'][0]['data'], '%Y-%m-%d %H:%M:%S')
        print("maschUpdated")
        print(maschUpdated)
        print("start_time")
        print(start_time)
        print("end_time")
        print(end_time)
        startDayTime = start_time.strftime('%Y-%m-%d %H:%M:%S')
        endDayTime = end_time.strftime('%Y-%m-%d %H:%M:%S')
        print("startDayTime")
        print(startDayTime)
        print("endDayTime")
        print(endDayTime)
        if startDayTime <= maschUpdated <= endDayTime:
            print("OK")
            recentRecords.append(record)

    debug.addToFileFull("worker", "ziggy", "export", "maschId", "filterbyDatetimeProducts", recentRecords)
    

def __main__():
    print("STARTING - WORKER")
    maschFlow()
    contentdeskFlow()
    
    
    
    print("END - WORKER")
    
if __name__== "__main__":
    __main__()