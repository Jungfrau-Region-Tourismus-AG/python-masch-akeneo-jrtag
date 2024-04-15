import datetime
import requests
import json
import sys
sys.path.append("..")

from service.objectStorage import getObject, putObject, countFilesInFolder, folderExist

from os import getenv
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())
MASCH_URL = getenv('MASCH_URL')
MASCH_PULL_URL = getenv('MASCH_PULL_URL')
MASCH_USER = getenv('MASCH_USER')
MASCH_PASSWORD = getenv('MASCH_PASSWORD')

def getMaschUpdateJobs():
    updateList = getObject('export/contentdesk/job/masch/updates/index.json')
    return updateList

def checkProductsMasch(updateList):
    print("Checking Masch UpdateList")
    updateListMasch = getMaschUpdateJobs()
    for checkProduct in updateList:
        print("Check product:")
        print(checkProduct)
        print("Action:")
        print(updateList[checkProduct]["action"])
        # Get Product from Object Storage
        product = getObject('export/contentdesk/products/'+checkProduct+'/index.json')
        print(product)
        # Check if MaschId exists
        if "maschId" in product["values"]:
            print("Product "+product["identifier"])
            print("MaschId: ")
            print(product["values"]["maschId"][0]["data"])
            maschId = product["values"]["maschId"][0]["data"]
            if maschId != "":
                try:
                     updateListMasch[product["identifier"]] = {"identifier": product["identifier"], "action": updateList[checkProduct]["action"]}
                except:
                    print("Product "+checkProduct+" --> Error")
                    # print exception
                    print(sys.exc_info()[0])

    print ("UpdateListMasch")
    print(updateListMasch)
    putObject(updateListMasch, 'export/contentdesk/job/masch/updates/index.json')

def transformAkeneotoMasch(akeneoProducts):
    print("Transforming Akeneo to Masch - transformAkeneotoMasch()")
    transformedProducts = {}
    transformedProducts['user_login'] = MASCH_USER
    transformedProducts['user_password'] = MASCH_PASSWORD
    transformedProducts['records'] = []
    for product in akeneoProducts:
        print("Product")
        print(product)
        print("In Product List")
        print(akeneoProducts[product]['identifier'])
        #print(product["values"]['maschId'][0]['data'])
        transformedProduct = {}
        #transformedProduct["identifier"] = product["identifier"]
        transformedProduct["record_id"] = akeneoProducts[product]["values"]['maschId'][0]['data']
        transformedProduct["created"] = akeneoProducts[product]["created"]
        transformedProduct["last_modifield"] = akeneoProducts[product]["updated"]
        transformedProduct["fields"] = {}
        # blog_seo_latitude
        transformedProduct["fields"][0] = {}
        transformedProduct["fields"][0]['field_name'] = "blog_seo_latitude"
        transformedProduct["fields"][0]['field_value'] = {}
        transformedProduct["fields"][0]['field_value']['de'] = akeneoProducts[product]["values"]['latitude'][0]['data']
        transformedProduct["fields"][0]['field_value']['en'] = akeneoProducts[product]["values"]['latitude'][0]['data']
        transformedProduct["fields"][0]['field_value']['fr'] = akeneoProducts[product]["values"]['latitude'][0]['data']
        # blog_seo_longitude
        transformedProduct["fields"][1] = {}
        transformedProduct["fields"][1]['field_name'] = "blog_seo_longitude"
        transformedProduct["fields"][1]['field_value'] = {}
        transformedProduct["fields"][1]['field_value']['de'] = akeneoProducts[product]["values"]['longitude'][0]['data']
        transformedProduct["fields"][1]['field_value']['en'] = akeneoProducts[product]["values"]['longitude'][0]['data']
        transformedProduct["fields"][1]['field_value']['fr'] = akeneoProducts[product]["values"]['longitude'][0]['data']
        transformedProducts['records'].append(transformedProduct)
    return transformedProducts

def postObjecttoMasch(product):
    url = MASCH_URL + MASCH_PULL_URL
    headers = {'Content-Type': 'application/json'}
    r = requests.post(url, json=product, headers=headers)
    print(r.status_code)
    print(r.text)
    print(json.decoder(r.json()))
    return r.json()

def loadObjectstoMasch(products):
    for product in products:
        postObjecttoMasch(product)
    print("DONE")