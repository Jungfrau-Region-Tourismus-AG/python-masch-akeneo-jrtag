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
from service.masch import getMaschUpdateJobs, checkProductsMasch, transformAkeneotoMasch, loadObjectstoMasch, postImagestoMasch

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
    #search = '{"maschId":[{"operator":"NOT EMPTY","value":""}],"maschUpdated":[{"operator":"BETWEEN","value":["' + startDayStr + '","' + endDayStr + '"]}]}'
    search = '{"maschId":[{"operator":"NOT EMPTY","value":""}],"maschUpdated":[{"operator":"BETWEEN","value":["' + startDayStr + '","' + endDayStr + '"]}],"updated":[{"operator":"SINCE LAST N DAYS","value":1}]}'
    print(search)
    contentdeskRecords = target.getProductBySearch(search)
    return contentdeskRecords

def getContentdeskProducts(env):
    targetCon = loadEnv(env)
    target = Akeneo(targetCon["host"], targetCon["clientId"], targetCon["secret"], targetCon["user"], targetCon["passwd"])
    search = '{"maschId":[{"operator":"NOT EMPTY","value":""}]}'
    products = target.getProducts(limit=100, search=search )
    return products

def updateContentdeskProducts(env, products):
    targetCon = loadEnv(env)
    target = Akeneo(targetCon["host"], targetCon["clientId"], targetCon["secret"], targetCon["user"], targetCon["passwd"])
    for item in products:
        print("     - Update Product: "+item['identifier'])
        body = {
            "identifier": item['identifier'],
            "values": {
                "maschUpdated": [
                    {
                        "data": datetime.datetime.now().isoformat()
                    }
                ]
            }
        }
        target.updateProduct(item['identifier'], body)

def checkContentdeskProductsbyDatetime(products):
    recentRecords = []
    for record in products:
        # string to datetime
        print("    - Check Product: "+record['identifier'])
        end_time = datetime.datetime.now()
        start_time = end_time - datetime.timedelta(minutes=5)
        updatedDateStr = record['updated']
        updatedDate = datetime.datetime.fromisoformat(updatedDateStr)
        maschUpdatedStr = record['values']['maschUpdated'][0]['data']
        maschUpdated = datetime.datetime.fromisoformat(maschUpdatedStr)
        maschUpdated = maschUpdated.strftime('%Y-%m-%d %H:%M:%S')
        updatedDate = updatedDate.strftime('%Y-%m-%d %H:%M:%S')
        startDayTime = start_time.strftime('%Y-%m-%d %H:%M:%S')
        endDayTime = end_time.strftime('%Y-%m-%d %H:%M:%S')
        print ("    - Start Time: " + startDayTime + " - End Time: " + endDayTime)
        print ("    - Updated: " + updatedDate)
        print ("    - Masch Updated: " + maschUpdated)
        if startDayTime <= updatedDate <= endDayTime:
            print("     - Add record to Update")
            if updatedDate != maschUpdated:
                print("     - Updated Date is not equal to Masch Updated Date")
                recentRecords.append(record)
    return recentRecords

def maschFlow():
    print (" - START: Masch Flow")
    maschRecords = getMaschPull()
    print(maschRecords)
    debug.addToFileFull("worker", "ziggy", "export", "maschId", "extractObjectsMasch", maschRecords)
    
    if maschRecords['result'] == 'success':
        if len(maschRecords['records']) > 0:
            # Update to Contentdesk
            print("   - START - UPDATE to Contentdesk")
            extractDataAkeneo = getContentdeskProducts("ziggy")
            debug.addToFileFull("worker", "ziggy", "export", "maschId", "extractDataAkeneo", extractDataAkeneo)
            
            print("   - TRANSFORMING to Contentdesk")
            transformDataAkeneo = transformAkeneotoMasch(extractDataAkeneo)
            transformData = transform(maschRecords, transformDataAkeneo)
            debug.addToFileFull("worker", "ziggy", "export", "maschId", "transformDataMasch", transformData)
            
            print("   - LOAD - Update to Contentdesk")
            loadData = load(transformData)
            debug.addToFileFull("worker", "ziggy", "export", "maschId", "loadObjectstoMasch", loadData)
            
            print("   - DONE - UPDATE to Contentdesk")
        else:
            print("   - No new records.")
            
    print(" - DONE: Masch Flow")
            
def contentdeskFlow(env):
    print (" - START: Contentdesk Flow")
    # CHECK
    contentdeskRecords = getContentdeskUpdatedProducts(env)
    debug.addToFileFull("worker", env, "export", "maschId", "extractProductsContentdesk", contentdeskRecords)
    
    # FILTER by datetime  
    recentRecords = checkContentdeskProductsbyDatetime(contentdeskRecords)
    debug.addToFileFull("worker", env, "export", "maschId", "filterbyDatetimeProductsContentdesk", recentRecords)
    
    # Transform to MASCH
    transformDataMASCH = transformAkeneotoMasch(recentRecords)
    debug.addToFileFull("worker", env, "export", "maschId", "transformDataMASCH", transformDataMASCH)
    
    # Update to MASCH
    print("   - Update to MASCH")
    loadObjectstoMasch(transformDataMASCH)
    
    ## Update Images to MASCH - Not needed
    print("   - POSTING IMAGES to MASCH")
    #postImagestoMasch(productList)
    
    # Update Contentesk Attribute MaschUpdated
    updateContentdeskProducts(env, recentRecords)
    
    print(" - DONE: Contentdesk Flow")
    
def __main__():
    print("STARTING - WORKER")
    maschFlow()
    contentdeskFlow("ziggy")
    print("END - WORKER")
    
if __name__== "__main__":
    __main__()