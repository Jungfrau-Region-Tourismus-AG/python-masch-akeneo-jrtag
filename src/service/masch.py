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

def setField(fieldname, field, value):
    field["fields"][0] = {}
    field["fields"][0]['field_name'] = fieldname
    field["fields"][0]['field_value']['de'] = akeneoProducts[product]["values"]['latitude'][0]['data']
    return field

def getValuebyLanguageScope(productAttribute, language, scope):
    for attribute in productAttribute:
        if attribute['locale'] == language and attribute['scope'] == scope:
            return attribute['data']
    return ""

def getValuebyLanguage(productAttribute, language):
    for attribute in productAttribute:
        if attribute['locale'] == language:
            return attribute['data']
    return ""

def getValuebyScope(productAttribute, scope):
    for attribute in productAttribute:
        if attribute['scope'] == scope:
            return attribute['data']
    return ""


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
        i = 0
        # MASCH: teaser_title_hotel_name / Akeneo: name
        if "name" in akeneoProducts[product]["values"]:
            transformedProduct["fields"][i] = {}
            transformedProduct["fields"][i]['field_name'] = "teaser_title_hotel_name"
            transformedProduct["fields"][i]['field_value'] = {}
            transformedProduct["fields"][i]['field_value']['de'] = getValuebyLanguage(akeneoProducts[product]["values"]['name'], "de_CH", "ecommerce")
            transformedProduct["fields"][i]['field_value']['en'] = getValuebyLanguage(akeneoProducts[product]["values"]['name'], "en_US", "ecommerce")
            transformedProduct["fields"][i]['field_value']['fr'] = getValuebyLanguage(akeneoProducts[product]["values"]['name'], "fr_FR", "ecommerce")
            i = i + 1
        # teaser_text_desktop / disambiguatingDescription
        if "disambiguatingDescription" in akeneoProducts[product]["values"]:
            transformedProduct["fields"][i] = {}
            transformedProduct["fields"][i]['field_name'] = "teaser_text_desktop"
            transformedProduct["fields"][i]['field_value'] = {}
            transformedProduct["fields"][i]['field_value']['de'] = getValuebyLanguageScope(akeneoProducts[product]["values"]['disambiguatingDescription'], "de_CH", "ecommerce")
            transformedProduct["fields"][i]['field_value']['en'] = getValuebyLanguageScope(akeneoProducts[product]["values"]['disambiguatingDescription'], "en_US", "ecommerce")
            transformedProduct["fields"][i]['field_value']['fr'] = getValuebyLanguageScope(akeneoProducts[product]["values"]['disambiguatingDescription'], "fr_FR", "ecommerce")
            i = i + 1
        # blog_table_description / description
        if "description" in akeneoProducts[product]["values"]:
            transformedProduct["fields"][i] = {}
            transformedProduct["fields"][i]['field_name'] = "blog_table_description"
            transformedProduct["fields"][i]['field_value'] = {}
            transformedProduct["fields"][i]['field_value']['de'] = getValuebyLanguageScope(akeneoProducts[product]["values"]['name'], "de_CH", "ecommerce")
            transformedProduct["fields"][i]['field_value']['en'] = getValuebyLanguageScope(akeneoProducts[product]["values"]['name'], "en_US", "ecommerce")
            transformedProduct["fields"][i]['field_value']['fr'] = getValuebyLanguageScope(akeneoProducts[product]["values"]['name'], "fr_FR", "ecommerce")
            i = i + 1
        # blog_seo_latitude / latitude
        if "latitude" in akeneoProducts[product]["values"]:
            transformedProduct["fields"][i] = {}
            transformedProduct["fields"][i]['field_name'] = "blog_seo_latitude"
            transformedProduct["fields"][i]['field_value'] = {}
            transformedProduct["fields"][i]['field_value']['de'] = akeneoProducts[product]["values"]['latitude'][0]['data']
            transformedProduct["fields"][i]['field_value']['en'] = akeneoProducts[product]["values"]['latitude'][0]['data']
            transformedProduct["fields"][i]['field_value']['fr'] = akeneoProducts[product]["values"]['latitude'][0]['data']
            i = i + 1
        # blog_seo_longitude / longitude
        if "longitude" in akeneoProducts[product]["values"]:
            transformedProduct["fields"][i] = {}
            transformedProduct["fields"][i]['field_name'] = "blog_seo_longitude"
            transformedProduct["fields"][i]['field_value'] = {}
            transformedProduct["fields"][i]['field_value']['de'] = akeneoProducts[product]["values"]['longitude'][0]['data']
            transformedProduct["fields"][i]['field_value']['en'] = akeneoProducts[product]["values"]['longitude'][0]['data']
            transformedProduct["fields"][i]['field_value']['fr'] = akeneoProducts[product]["values"]['longitude'][0]['data']
            i = i + 1
        # teaser_title_hotel_place / addressLocality
        if "addressLocality" in akeneoProducts[product]["values"]:
            transformedProduct["fields"][i] = {}
            transformedProduct["fields"][i]['field_name'] = "teaser_title_hotel_place"
            transformedProduct["fields"][i]['field_value'] = {}
            transformedProduct["fields"][i]['field_value']['de'] = akeneoProducts[product]["values"]['addressLocality'][0]['data']
            transformedProduct["fields"][i]['field_value']['en'] = akeneoProducts[product]["values"]['addressLocality'][0]['data']
            transformedProduct["fields"][i]['field_value']['fr'] = akeneoProducts[product]["values"]['addressLocality'][0]['data']
            i = i + 1
        # blog_table_contact_details_phone / telephone
        if "telephone" in akeneoProducts[product]["values"]:
            transformedProduct["fields"][i] = {}
            transformedProduct["fields"][i]['field_name'] = "blog_table_contact_details_phone"
            transformedProduct["fields"][i]['field_value'] = {}
            transformedProduct["fields"][i]['field_value']['de'] = getValuebyScope(akeneoProducts[product]["values"]['telephone'], "ecommerce")
            transformedProduct["fields"][i]['field_value']['en'] = getValuebyScope(akeneoProducts[product]["values"]['telephone'], "ecommerce")
            transformedProduct["fields"][i]['field_value']['fr'] = getValuebyScope(akeneoProducts[product]["values"]['telephone'], "ecommerce")
            i = i + 1
        # blog_table_contact_email / email
        if "email" in akeneoProducts[product]["values"]:
            transformedProduct["fields"][i] = {}
            transformedProduct["fields"][i]['field_name'] = "blog_table_contact_email"
            transformedProduct["fields"][i]['field_value'] = {}
            transformedProduct["fields"][i]['field_value']['de'] = getValuebyScope(akeneoProducts[product]["values"]['email'], "ecommerce")
            transformedProduct["fields"][i]['field_value']['en'] = getValuebyScope(akeneoProducts[product]["values"]['email'], "ecommerce")
            transformedProduct["fields"][i]['field_value']['fr'] = getValuebyScope(akeneoProducts[product]["values"]['email'], "ecommerce")
            i = i + 1
        # metaserver_hotel_website / url
        if "url" in akeneoProducts[product]["values"]:
            transformedProduct["fields"][i] = {}
            transformedProduct["fields"][i]['field_name'] = "metaserver_hotel_website"
            transformedProduct["fields"][i]['field_value'] = {}
            transformedProduct["fields"][i]['field_value']['de'] = getValuebyScope(akeneoProducts[product]["values"]['url'], "ecommerce")
            transformedProduct["fields"][i]['field_value']['en'] = getValuebyScope(akeneoProducts[product]["values"]['url'], "ecommerce")
            transformedProduct["fields"][i]['field_value']['fr'] = getValuebyScope(akeneoProducts[product]["values"]['url'], "ecommerce")
            i = i + 1
        # TODO metaserver_trustyou_id / trustyouId


        transformedProducts['records'].append(transformedProduct)
        print(transformedProduct)
    print(transformedProducts)
    return transformedProducts

def postObjecttoMasch(product):
    url = MASCH_URL + MASCH_PULL_URL
    headers = {'Content-Type': 'application/json'}
    r = requests.post(url, json=product, headers=headers)
    print(r.status_code)
    #print(r.text)
    #print(json.decoder(r.json()))
    return r.status_code

def loadObjectstoMasch(products):
    postObjecttoMasch(products)
    print("DONE")