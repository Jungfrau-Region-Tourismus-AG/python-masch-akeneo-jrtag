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
        transformedProduct["record_name"] = akeneoProducts[product]["values"]['maschName'][0]['data']
        transformedProduct["record_id"] = akeneoProducts[product]["values"]['maschId'][0]['data']
        #transformedProduct["created"] = akeneoProducts[product]["created"]
        #transformedProduct["last_modifield"] = akeneoProducts[product]["updated"]
        transformedProduct["external_uid"] = akeneoProducts[product]['identifier']
        transformedProduct["active"] = 1
        transformedProduct["fields"] = []
        i = 0
        # MASCH: teaser_title_hotel_name / Akeneo: name
        if "name" in akeneoProducts[product]["values"]:
            nameValue = {}
            nameValue['field_name'] = "teaser_title_hotel_name"
            nameValue['field_type'] = "1_line_text"
            nameValue['field_value'] = {}
            nameValue['field_value']['de'] = getValuebyLanguage(akeneoProducts[product]["values"]['name'], "de_CH")
            nameValue['field_value']['en'] = getValuebyLanguage(akeneoProducts[product]["values"]['name'], "en_US")
            nameValue['field_value']['fr'] = getValuebyLanguage(akeneoProducts[product]["values"]['name'], "fr_FR")
            transformedProduct["fields"].append(nameValue)
            i = i + 1
        # teaser_text_desktop / disambiguatingDescription
        if "disambiguatingDescription" in akeneoProducts[product]["values"]:
            disambiguatingDescription = {}
            disambiguatingDescription['field_name'] = "teaser_text_desktop"
            disambiguatingDescription['field_type'] = "multiline_text"
            disambiguatingDescription['field_value'] = {}
            disambiguatingDescription['field_value']['de'] = getValuebyLanguageScope(akeneoProducts[product]["values"]['disambiguatingDescription'], "de_CH", "ecommerce")
            disambiguatingDescription['field_value']['en'] = getValuebyLanguageScope(akeneoProducts[product]["values"]['disambiguatingDescription'], "en_US", "ecommerce")
            disambiguatingDescription['field_value']['fr'] = getValuebyLanguageScope(akeneoProducts[product]["values"]['disambiguatingDescription'], "fr_FR", "ecommerce")
            transformedProduct["fields"].append(disambiguatingDescription)
        # blog_table_description / description
        if "description" in akeneoProducts[product]["values"]:
            description = {}
            description['field_name'] = "blog_table_description"
            description['field_type'] = "multiline_text"
            description['field_value'] = {}
            description['field_value']['de'] = getValuebyLanguageScope(akeneoProducts[product]["values"]['description'], "de_CH", "ecommerce")
            description['field_value']['en'] = getValuebyLanguageScope(akeneoProducts[product]["values"]['description'], "en_US", "ecommerce")
            description['field_value']['fr'] = getValuebyLanguageScope(akeneoProducts[product]["values"]['description'], "fr_FR", "ecommerce")
            transformedProduct["fields"].append(description)
        # blog_seo_latitude / latitude
        if "latitude" in akeneoProducts[product]["values"]:
            latitude = {}
            latitude['field_name'] = "blog_seo_latitude"
            latitude['field_type'] = "1_line_text"
            latitude['readonly'] = 0
            latitude['description'] = None
            latitude['field_value'] = {}
            latitude['field_value']['de'] = akeneoProducts[product]["values"]['latitude'][0]['data']
            latitude['field_value']['en'] = akeneoProducts[product]["values"]['latitude'][0]['data']
            latitude['field_value']['fr'] = akeneoProducts[product]["values"]['latitude'][0]['data']
            transformedProduct["fields"].append(latitude)
        # blog_seo_longitude / longitude
        if "longitude" in akeneoProducts[product]["values"]:
            longitude = {}
            longitude['field_name'] = "blog_seo_longitude"
            longitude['field_type'] = "1_line_text"
            longitude['readonly'] = 0
            longitude['description'] = None
            longitude['field_value'] = {}
            longitude['field_value']['de'] = akeneoProducts[product]["values"]['longitude'][0]['data']
            longitude['field_value']['en'] = akeneoProducts[product]["values"]['longitude'][0]['data']
            longitude['field_value']['fr'] = akeneoProducts[product]["values"]['longitude'][0]['data']
            transformedProduct["fields"].append(longitude)
        # teaser_title_hotel_place / addressLocality
        if "addressLocality" in akeneoProducts[product]["values"]:
            addressLocality = {}
            addressLocality['field_name'] = "teaser_title_hotel_place"
            addressLocality['field_type'] = "1_line_text"
            addressLocality['field_value'] = {}
            addressLocality['field_value']['de'] = akeneoProducts[product]["values"]['addressLocality'][0]['data']
            addressLocality['field_value']['en'] = akeneoProducts[product]["values"]['addressLocality'][0]['data']
            addressLocality['field_value']['fr'] = akeneoProducts[product]["values"]['addressLocality'][0]['data']
            transformedProduct["fields"].append(addressLocality)
        # blog_table_contact_details_phone / telephone
        if "telephone" in akeneoProducts[product]["values"]:
            telephone = {}
            telephone['field_name'] = "blog_table_contact_details_phone"
            telephone['field_type'] = "1_line_text"
            telephone['field_value'] = {}
            telephone['field_value']['de'] = getValuebyScope(akeneoProducts[product]["values"]['telephone'], "ecommerce")
            telephone['field_value']['en'] = getValuebyScope(akeneoProducts[product]["values"]['telephone'], "ecommerce")
            telephone['field_value']['fr'] = getValuebyScope(akeneoProducts[product]["values"]['telephone'], "ecommerce")
            transformedProduct["fields"].append(telephone)
        # blog_table_contact_email / email
        if "email" in akeneoProducts[product]["values"]:
            email = {}
            email['field_name'] = "blog_table_contact_email"
            email['field_type'] = "url_link"
            email['field_value'] = {}
            email['field_value']['de'] = getValuebyScope(akeneoProducts[product]["values"]['email'], "ecommerce")
            email['field_value']['en'] = getValuebyScope(akeneoProducts[product]["values"]['email'], "ecommerce")
            email['field_value']['fr'] = getValuebyScope(akeneoProducts[product]["values"]['email'], "ecommerce")
            transformedProduct["fields"].append(email)
        # metaserver_hotel_website / url
        if "url" in akeneoProducts[product]["values"]:
            url = {}
            url['field_name'] = "metaserver_hotel_website"
            url['field_type'] = "url_link"
            url['field_value'] = {}
            url['field_value']['de'] = getValuebyScope(akeneoProducts[product]["values"]['url'], "ecommerce")
            url['field_value']['en'] = getValuebyScope(akeneoProducts[product]["values"]['url'], "ecommerce")
            url['field_value']['fr'] = getValuebyScope(akeneoProducts[product]["values"]['url'], "ecommerce")
            transformedProduct["fields"].append(url)
        # TODO metaserver_trustyou_id / trustyouId


        transformedProducts['records'].append(transformedProduct)
        print(transformedProduct)
    #print(transformedProducts)
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