# Update to MASCH all 5 minutes
import json
import sys
sys.path.append("..")

from service.masch import masch

def __main__():
    print("STARTING - WORKER")
    # 1. Check last changes all Products with maschId in Akeneo
    # 1. Check Masch 
    maschRecords = masch.getMaschPull()
    print(maschRecords)
    if len(maschRecords['records']) > 0:
        # Update to Contentdesk
        print("UPDATE to Contentdesk")
    else:
        print("No new records")
    
    
    print("END - WORKER")
    
if __name__== "__main__":
    __main__()