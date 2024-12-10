# Contentdesk Flow
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
import service.contentdesk as contentdesk

def checkContentdeskProductsbyDatetime(products):
    recentRecords = []
    for item in products:
        # string to datetime
        print("    * CHECK Product: "+item['identifier'])
        end_time = datetime.datetime.now()
        start_time = end_time - datetime.timedelta(minutes=10)
        updatedDateStr = item['updated']
        updatedDateDatetime = datetime.datetime.fromisoformat(updatedDateStr)
        updatedDate = updatedDateDatetime.strftime('%Y-%m-%d %H:%M')
        
        maschUpdatedStr = item['values']['maschUpdated'][0]['data']
        maschUpdatedDatetime = datetime.datetime.fromisoformat(maschUpdatedStr)
        maschUpdated = maschUpdatedDatetime.strftime('%Y-%m-%d %H:%M')

        startDayTime = start_time.strftime('%Y-%m-%d %H:%M')
        endDayTime = end_time.strftime('%Y-%m-%d %H:%M')
        
        print("    - Updated Date Check: " + startDayTime + " <= " + updatedDate + " <= " + endDayTime)
        if startDayTime <= updatedDate <= endDayTime:
            print("    - Item Updated in last 10 minutes")
            print("    - COMPARE")
            print("    - Start Time: " + startDayTime + " - End Time: " + endDayTime)
            print("    - Updated: " + updatedDate)
            print("    - Masch Updated: " + maschUpdated)
            if updatedDate != maschUpdated:
                print("     - Add record to Update")
                time_difference = abs((updatedDateDatetime - maschUpdatedDatetime).total_seconds() / 60)
                if time_difference > 5:
                    print("     - Time difference is greater than 5 minutes")
                    recentRecords.append(item)
                else:
                    print("     - Time difference is not greater than 5 minutes")
            else:
                print("     - Updated Date is equal to Masch Updated Date")
    return recentRecords

def contentdeskFlow():
    print (" - START: Contentdesk Flow")
    # DEBUG
    env = 'ziggy' 
    # CHECK
    contentdeskRecords = contentdesk.getContentdeskUpdatedProducts()
    debug.addToFileFull("worker", env, "export", "maschId", "extractProductsContentdesk", contentdeskRecords)
    
    # FILTER by datetime
    recentRecords = checkContentdeskProductsbyDatetime(contentdeskRecords)
    debug.addToFileFull("worker", env, "export", "maschId", "filterbyDatetimeProductsContentdesk", recentRecords)
    
    if len(recentRecords) == 0:
        print("   - No new records to update.")
    else:
        # Transform to MASCH
        print("   - Transform to MASCH")
        transformDataMASCH = masch.transformAkeneotoMasch(recentRecords)
        debug.addToFileFull("worker", env, "export", "maschId", "transformDataMASCH", transformDataMASCH)
        
        # Update to MASCH
        print("   - Update to MASCH")
        masch.loadObjectstoMasch(transformDataMASCH)
        
        ## Update Images to MASCH - Not needed
        print("   - POSTING IMAGES to MASCH")
        print("   - TODO: POSTING IMAGES to MASCH")
        masch.postImagestoMasch(recentRecords)
    
        # Update Contentesk Attribute MaschUpdated
        print("   - Update Contentdesk Object - maschUpdated")
        contentdesk.updateContentdeskProducts(recentRecords)
    
    print(" - DONE: Contentdesk Flow")