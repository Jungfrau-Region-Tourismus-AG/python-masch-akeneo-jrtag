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
import service.objectStorage as objectStorage

def checkContentdeskProductsbyDatetime(products):
    recentRecords = []
    for item in products:
        # string to datetime
        print("    * CHECK Product: "+item['identifier'])
        if item['identifier'] == "f7be1227-d085-42a2-95f5-236b54ac14b0":
            end_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
            start_time = end_time - datetime.timedelta(minutes=15)
            updatedDateStr = item['updated']
            updatedDateDatetime = datetime.datetime.fromisoformat(updatedDateStr)
            updatedDate = updatedDateDatetime.strftime('%Y-%m-%d %H:%M')
            
            if 'values' in item:
                if 'maschUpdated' in item['values']:
                    maschUpdatedStr = item['values']['maschUpdated'][0]['data']
                    maschUpdatedDatetime = datetime.datetime.fromisoformat(maschUpdatedStr)
                    maschUpdated = maschUpdatedDatetime.strftime('%Y-%m-%d %H:%M')
                else:
                    maschUpdated = datetime.timedelta(days=-1)

            startDayTime = start_time.strftime('%Y-%m-%d %H:%M')
            endDayTime = end_time.strftime('%Y-%m-%d %H:%M')
            
            print("    - Updated Date Check: " + startDayTime + " <= " + updatedDate + " <= " + endDayTime)
            if startDayTime <= updatedDate <= endDayTime:
                print("    - Item Updated in last 10 minutes")
                print("    - COMPARE")
                print("    - Start Time: " + startDayTime + " - End Time: " + endDayTime)
                print("    - Updated: " + updatedDate)
                print("    - Masch Updated: " + str(maschUpdated))
                if updatedDate != maschUpdated:
                    print("     - Add record to Update")
                    time_difference = abs((updatedDateDatetime - maschUpdatedDatetime).total_seconds() / 60)
                    if time_difference > 2:
                        print("     - Time difference is greater than 2 minutes")
                        recentRecords.append(item)
                    else:
                        print("     - Time difference is not greater than 2 minutes")
                else:
                    print("     - Updated Date is equal to Masch Updated Date")
            recentRecords.append(item)
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
        # Backup to Object Storage
        print("   - Backup to Object Storage")
        current_datetime = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H-%M-%S")
        str_current_datetime = str(current_datetime)
        objectStorage.exportProduct(recentRecords, 'export/contentdesk/worker/contentdeskFlow/'+str_current_datetime, "contentdeskExport")
        
        # Transform to MASCH
        print("   - Transform to MASCH")
        transformDataMASCH = masch.transformAkeneotoMasch(recentRecords)
        debug.addToFileFull("worker", env, "export", "maschId", "transformDataMASCH", transformDataMASCH)
        
        # Update to MASCH
        print("   - Update to MASCH")
        masch.loadObjectstoMasch(transformDataMASCH)
        
        ## Update Images to MASCH - Not needed
        print("   - POSTING IMAGES to MASCH")
        print("   - TODO: POSTING IMAGES (Gallery) to MASCH")
        #masch.postImagestoMasch(recentRecords)
    
        # Update Contentesk Attribute MaschUpdated
        print("   - Update Contentdesk Object - maschUpdated")
        contentdesk.updateContentdeskProducts(recentRecords)
    
    print(" - DONE: Contentdesk Flow")
    
    
def contentdeskFullFlow():
    print (" - START: Contentdesk Flow")
    # DEBUG
    env = 'ziggy' 
    # CHECK
    contentdeskRecords = contentdesk.getContentdeskallMASCHProducts()
    debug.addToFileFull("worker", env, "export", "maschId", "extractProductsContentdesk", contentdeskRecords)
    
    # FILTER by datetime
    #recentRecords = checkContentdeskProductsbyDatetime(contentdeskRecords)
    #debug.addToFileFull("worker", env, "export", "maschId", "filterbyDatetimeProductsContentdesk", recentRecords)
    
    recentRecords = contentdeskRecords
    
    if len(recentRecords) == 0:
        print("   - No new records to update.")
    else:
        # Backup to Object Storage
        print("   - Backup to Object Storage")
        current_datetime = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H-%M-%S")
        str_current_datetime = str(current_datetime)
        objectStorage.exportProduct(recentRecords, 'export/contentdesk/worker/contentdeskFlow/'+str_current_datetime, "contentdeskExport")
        
        # Transform to MASCH
        print("   - Transform to MASCH")
        transformDataMASCH = masch.transformAkeneotoMasch(recentRecords)
        debug.addToFileFull("worker", env, "export", "maschId", "transformDataMASCH", transformDataMASCH)
        
        # Update to MASCH
        print("   - Update to MASCH")
        masch.loadObjectstoMasch(transformDataMASCH)
        
        ## Update Images to MASCH - Not needed
        print("   - POSTING IMAGES to MASCH")
        print("   - TODO: POSTING IMAGES (Gallery) to MASCH")
        masch.postImagestoMasch(recentRecords)
    
        # Update Contentesk Attribute MaschUpdated
        print("   - Update Contentdesk Object - maschUpdated")
        contentdesk.updateContentdeskProducts(recentRecords)
    
    print(" - DONE: Contentdesk Flow")