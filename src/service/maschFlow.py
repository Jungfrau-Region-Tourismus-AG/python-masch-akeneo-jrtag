# Masch Flow
import datetime
import sys
sys.path.append("..")

import service.debug as debug
import service.contentdesk as contentdesk
import service.contentdeskFlow as contentdeskFlow
import service.masch as masch
from service.transform import transform, transformAkeneotoMasch

def compareModifiedDates(maschRecords, extractDataAkeneo):
    recentRecords = []
    
    for item in maschRecords:
        maschId = item['record_id']
        #sku = item['external_uid']
        maschUpdatedStr = item['last_modified']
        maschUpdatedDatetime = datetime.datetime.fromisoformat(maschUpdatedStr)
        maschUpdated = maschUpdatedDatetime.strftime('%Y-%m-%d %H:%M')
        
        # Filter extractDataAkeneo by maschId
        akeneoObject = [product for product in extractDataAkeneo if 'values' in product and 'maschId' in product['values'] and product['values']['maschId'][0]['data'] == maschId]
        print("      - Check Object Modified Date: "+str(maschId))
        if len(akeneoObject) > 0:
            print("   - Filtered by maschId: "+maschId)
            print(akeneoObject)
            updatedDateStr = akeneoObject[0]['updated']
            updatedDateDatetime = datetime.datetime.fromisoformat(updatedDateStr)
            updatedDate = updatedDateDatetime.strftime('%Y-%m-%d %H:%M')
            print("    - COMPARE - Updated: " + updatedDate + " - Masch Updated: " + maschUpdated)
            if updatedDate != maschUpdated:
                time_difference = abs((updatedDateDatetime - maschUpdatedDatetime).total_seconds() / 60)
                if time_difference > 2:
                    recentRecords.append(akeneoObject[0])
    
    return recentRecords

def maschFlow():
    print (" - START: Masch Flow")
    maschRecords = masch.getMaschPull()
    #print(maschRecords)
    # DEBUG
    env = "ziggy"
    debug.addToFileFull("worker", env, "export", "maschId", "extractObjectsMasch", maschRecords)
    
    if maschRecords['result'] == 'success':
        if len(maschRecords['records']) > 0:
            # Update to Contentdesk
            print("   - START - UPDATE to Contentdesk")
            extractDataAkeneo = contentdesk.getContentdeskProducts()
            debug.addToFileFull("worker", env, "export", "maschId", "extractDataAkeneo", extractDataAkeneo)
            
            # COMPARE modified date
            recentRecords = compareModifiedDates(maschRecords['records'], extractDataAkeneo)
            debug.addToFileFull("worker", env, "export", "maschId", "compareModifiedDates", recentRecords)
            
            if len(recentRecords) == 0:
                print("   - No new records to update.")
            else:
                print("   - TRANSFORMING to Contentdesk")
                transformData = transform(maschRecords, extractDataAkeneo)
                debug.addToFileFull("worker", env, "export", "maschId", "transformDataAkeneo", transformData)
                    
                print("   - LOAD - Update to Contentdesk")
                #TODO: Implement load function
                #loadData = load(transformData)
                contentdesk.updateContentdeskProducts(recentRecords)
                debug.addToFileFull("worker", "ziggy", "export", "maschId", "MASCHupdateContentdeskProducts", recentRecords)
                    
                print("   - DONE - UPDATE to Contentdesk")
        else:
            print("   - No new records.")
            
    print(" - DONE: Masch Flow")