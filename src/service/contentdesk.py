import json
import datetime
from akeneo.akeneo import Akeneo

from os import getenv
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

import sys
sys.path.append("..")
import service.debug as debug
import service.masch as masch

AKENEO_HOST = getenv('AKENEO_HOST')
AKENEO_CLIENT_ID = getenv('AKENEO_CLIENT_ID')
AKENEO_CLIENT_SECRET = getenv('AKENEO_CLIENT_SECRET')
AKENEO_USERNAME = getenv('AKENEO_USERNAME')
AKENEO_PASSWORD = getenv('AKENEO_PASSWORD')

def getContentdeskUpdatedProducts():
    target = Akeneo(AKENEO_HOST, AKENEO_CLIENT_ID, AKENEO_CLIENT_SECRET, AKENEO_USERNAME, AKENEO_PASSWORD)
    
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

def getContentdeskProducts():
    target = Akeneo(AKENEO_HOST, AKENEO_CLIENT_ID, AKENEO_CLIENT_SECRET, AKENEO_USERNAME, AKENEO_PASSWORD)
    
    search = '{"maschId":[{"operator":"NOT EMPTY","value":""}]}'
    products = target.getProducts(limit=100, search=search )
    return products

def updateContentdeskProducts(products):
    target = Akeneo(AKENEO_HOST, AKENEO_CLIENT_ID, AKENEO_CLIENT_SECRET, AKENEO_USERNAME, AKENEO_PASSWORD)
    
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
        target.patchProductByCode(item['identifier'], body)

def checkContentdeskProductsbyDatetime(products):
    recentRecords = []
    for item in products:
        # string to datetime
        print("    - Check Product: "+item['identifier'])
        end_time = datetime.datetime.now()
        start_time = end_time - datetime.timedelta(minutes=5)
        updatedDateStr = item['updated']
        updatedDate = datetime.datetime.fromisoformat(updatedDateStr)
        updatedDate = updatedDate.strftime('%Y-%m-%d %H:%M:%S')
        
        maschUpdatedStr = item['values']['maschUpdated'][0]['data']
        maschUpdated = datetime.datetime.fromisoformat(maschUpdatedStr)
        maschUpdated = maschUpdated.strftime('%Y-%m-%d %H:%M:%S')

        startDayTime = start_time.strftime('%Y-%m-%d %H:%M:%S')
        endDayTime = end_time.strftime('%Y-%m-%d %H:%M:%S')
        print ("    - Start Time: " + startDayTime + " - End Time: " + endDayTime)
        print ("    - Updated: " + updatedDate)
        print ("    - Masch Updated: " + maschUpdated)
        
        if updatedDate >= start_time.strftime('%Y-%m-%d %H:%M:%S') and updatedDate <= end_time.strftime('%Y-%m-%d %H:%M:%S'):
            print("     - Item Updated in last 5min")
        
        if startDayTime <= updatedDate <= endDayTime:
            print("     - Add record to Update")
            if updatedDate != maschUpdated:
                print("     - Updated Date is not equal to Masch Updated Date")
                recentRecords.append(item)
    return recentRecords

def contentdeskFlow():
    print (" - START: Contentdesk Flow")
    # DEBUG
    env = 'ziggy' 
    # CHECK
    contentdeskRecords = getContentdeskUpdatedProducts()
    debug.addToFileFull("worker", env, "export", "maschId", "extractProductsContentdesk", contentdeskRecords)
    
    # FILTER by datetime
    recentRecords = checkContentdeskProductsbyDatetime(contentdeskRecords)
    debug.addToFileFull("worker", env, "export", "maschId", "filterbyDatetimeProductsContentdesk", recentRecords)
    
    if len(recentRecords) == 0:
        print("   - No new records to update.")
        return
    
    # Transform to MASCH
    print("   - Transform to MASCH")
    transformDataMASCH = masch.transformAkeneotoMasch(recentRecords)
    debug.addToFileFull("worker", env, "export", "maschId", "transformDataMASCH", transformDataMASCH)
    
    # Update to MASCH
    print("   - Update to MASCH")
    #masch.loadObjectstoMasch(transformDataMASCH)
    
    ## Update Images to MASCH - Not needed
    print("   - POSTING IMAGES to MASCH")
    #postImagestoMasch(productList)
    
    # Update Contentesk Attribute MaschUpdated
    updateContentdeskProducts(recentRecords)
    
    print(" - DONE: Contentdesk Flow")