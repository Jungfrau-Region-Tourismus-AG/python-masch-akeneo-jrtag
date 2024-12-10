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
    search = '{"maschId":[{"operator":"NOT EMPTY","value":""}],"updated":[{"operator":"SINCE LAST N DAYS","value":1}]}'
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
        #print("     - Update Product: "+item['identifier'])
        body = {
            "identifier": item['identifier'],
            "values": {
                "maschUpdated": [
                    {
                        "locale": None,
                        "scope": None,
                        "data": datetime.datetime.now().isoformat()
                    }
                ]
            }
        }
        response = target.patchProductByCode(item['identifier'], body)
        print("   - Response: "+str(response))
    
