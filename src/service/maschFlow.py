# Masch Flow
import sys
sys.path.append("..")

import service.debug as debug
import service.contentdesk as contentdesk
import service.masch as masch
from service.transform import transform, transformAkeneotoMasch

def maschFlow():
    print (" - START: Masch Flow")
    maschRecords = masch.getMaschPull()
    #print(maschRecords)
    debug.addToFileFull("worker", "ziggy", "export", "maschId", "extractObjectsMasch", maschRecords)
    
    if maschRecords['result'] == 'success':
        if len(maschRecords['records']) > 0:
            # Update to Contentdesk
            print("   - START - UPDATE to Contentdesk")
            extractDataAkeneo = contentdesk.getContentdeskProducts()
            debug.addToFileFull("worker", "ziggy", "export", "maschId", "extractDataAkeneo", extractDataAkeneo)
            
            print("   - TRANSFORMING to Contentdesk")
            transformData = transform(maschRecords, extractDataAkeneo)
            debug.addToFileFull("worker", "ziggy", "export", "maschId", "transformDataAkeneo", transformData)
            
            print("   - LOAD - Update to Contentdesk")
            #TODO: Implement load function
            #loadData = load(transformData)
            #debug.addToFileFull("worker", "ziggy", "export", "maschId", "loadData", loadData)
            
            print("   - DONE - UPDATE to Contentdesk")
        else:
            print("   - No new records.")
            
    print(" - DONE: Masch Flow")