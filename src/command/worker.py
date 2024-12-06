# Update to MASCH all 5 minutes
import json
import datetime
from akeneo.akeneo import Akeneo
import sys
sys.path.append("..")

from service.masch import getMaschPull
from service.loadEnv import loadEnv
import service.debug as debug
from service.objectStorage import getObject, getObjects, putObject, countFilesInFolder, folderExist

from extract import extract, getAkeneoProducts
from transform import transform, transformAkeneotoMasch
from load import load

def getContentdeskUpdatedProducts(env):
    targetCon = loadEnv(env)
    target = Akeneo(targetCon["host"], targetCon["clientId"], targetCon["secret"], targetCon["user"], targetCon["passwd"])
    search = '{"labels":[{"operator":"NOT EMPTY","value":""}]}&attributes=labels'
    end_time = datetime.datetime.now()
    start_time = end_time - datetime.timedelta(minutes=5)
    startDay = end_time - datetime.timedelta(days=1)
    endDayStr = end_time.strftime("%Y-%m-%d")
    startDayStr = startDay.strftime("%Y-%m-%d")
    search = '{"maschId":[{"operator":"NOT EMPTY","value":""}],"maschUpdated":[{"operator":"BETWEEN","value":["' + startDayStr + '","' + endDayStr + '"]}]}'
    print(search)
    contentdeskRecords = target.getProductBySearch(search)
    return contentdeskRecords

def getContentdeskProducts(env):
    targetCon = loadEnv(env)
    target = Akeneo(targetCon["host"], targetCon["clientId"], targetCon["secret"], targetCon["user"], targetCon["passwd"])
    search = '{"maschId":[{"operator":"NOT EMPTY","value":""}]}'
    products = target.getProducts(limit=100, search=search )
    return products

def checkContentdeskProductsbyDatetime(products):
    recentRecords = []
    for record in products:
        # string to datetime
        end_time = datetime.datetime.now()
        start_time = end_time - datetime.timedelta(minutes=5)
        maschUpdatedStr = record['values']['maschUpdated'][0]['data']
        maschUpdated = datetime.datetime.fromisoformat(maschUpdatedStr)
        maschUpdated = maschUpdated.strftime('%Y-%m-%d %H:%M:%S')
        startDayTime = start_time.strftime('%Y-%m-%d %H:%M:%S')
        endDayTime = end_time.strftime('%Y-%m-%d %H:%M:%S')
        if startDayTime <= maschUpdated <= endDayTime:
            print("Add record to Update")
            recentRecords.append(record)
    return recentRecords

def maschFlow():
    print ("Masch Flow")
    maschRecords = getMaschPull()
    print(maschRecords)
    debug.addToFileFull("worker", "ziggy", "export", "maschId", "extractObjectsMasch", maschRecords)
    
    if maschRecords['result'] == 'success':
        if len(maschRecords['records']) > 0:
            # Update to Contentdesk
            print("START - UPDATE to Contentdesk")
            # TODO: Update to Contentdesk
            extractDataAkeneo = getContentdeskProducts("ziggy")
            print("TRANSFORMING to Contentdesk")
            transformDataAkeneo = transformAkeneotoMasch(extractDataAkeneo)
            transformData = transform(maschRecords, transformDataAkeneo)
            debug.addToFileFull("worker", "ziggy", "export", "maschId", "transformDataMasch", transformData)
            print("LOADING to Contentdesk")
            loadData = load(transformData)
            debug.addToFileFull("worker", "ziggy", "export", "maschId", "loadObjectstoMasch", loadData)
            print("DONE")
        else:
            print("No new records.")
            
def contentdeskFlow():
    print ("Contentdesk Flow")
    # CHECK
    contentdeskRecords = getContentdeskUpdatedProducts("ziggy")
    debug.addToFileFull("worker", "ziggy", "export", "maschId", "extractProductsContentdesk", contentdeskRecords)
    
    # FILTER by datetime  
    recentRecords = checkContentdeskProductsbyDatetime(contentdeskRecords)
    debug.addToFileFull("worker", "ziggy", "export", "maschId", "filterbyDatetimeProductsContentdesk", recentRecords)
    
    # Update to MASCH

def __main__():
    print("STARTING - WORKER")
    maschFlow()
    contentdeskFlow()
    
    
    
    print("END - WORKER")
    
if __name__== "__main__":
    __main__()