import datetime
import requests
import json
import sys
sys.path.append("..")

import service.debug as debug
import service.contentdesk as contentdesk
#from service.transform import transform, transformAkeneotoMasch
from service.objectStorage import getObject, putObject, countFilesInFolder, folderExist, getObjectUrl

from os import getenv
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

MASCH_URL = getenv('MASCH_URL')
MASCH_PULL_URL = getenv('MASCH_PULL_URL')
MASCH_PUSH_URL = getenv('MASCH_PUSH_URL')
MASCH_USER = getenv('MASCH_USER')
MASCH_PASSWORD = getenv('MASCH_PASSWORD')

def getMaschPull():
    url = MASCH_URL + MASCH_PULL_URL
    end_time = datetime.datetime.now()
    start_time = end_time - datetime.timedelta(minutes=5)
    body = {
        "user_login": MASCH_USER,
        "user_password": MASCH_PASSWORD,
        "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S")
    }
    r = requests.get(url, json=body)
    print(r.status_code)
    return r.json()

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
        print(product['identifier'])
        #print(product)
        #print("In Product List")
        #print(product['identifier'])
        transformedProduct = {}
        if "maschId" in product["values"]:
            transformedProduct["record_id"] = product["values"]['maschId'][0]['data']
        if "maschName" in product["values"]:
            transformedProduct["record_name"] = product["values"]['maschName'][0]['data']
        transformedProduct["created"] = product["created"]
        transformedProduct["last_modifield"] = product["updated"]
        transformedProduct["external_uid"] = product['identifier']
        transformedProduct["active"] = 1
        transformedProduct["fields"] = []
        i = 0
        # MASCH: teaser_title_hotel_name / Akeneo: name
        if "name" in product["values"]:
            nameValue = {}
            nameValue['field_name'] = "teaser_title_hotel_name"
            nameValue['field_type'] = "1_line_text"
            nameValue['field_value'] = {}
            nameValue['field_value']['de'] = getValuebyLanguage(product["values"]['name'], "de_CH")
            nameValue['field_value']['en'] = getValuebyLanguage(product["values"]['name'], "en_US")
            nameValue['field_value']['fr'] = getValuebyLanguage(product["values"]['name'], "fr_FR")
            transformedProduct["fields"].append(nameValue)
            i = i + 1
        # teaser_text_desktop / disambiguatingDescription
        if "disambiguatingDescription" in product["values"]:
            disambiguatingDescription = {}
            disambiguatingDescription['field_name'] = "teaser_text_desktop"
            disambiguatingDescription['field_type'] = "multiline_text"
            disambiguatingDescription['field_value'] = {}
            disambiguatingDescription['field_value']['de'] = getValuebyLanguageScope(product["values"]['disambiguatingDescription'], "de_CH", "ecommerce")
            disambiguatingDescription['field_value']['en'] = getValuebyLanguageScope(product["values"]['disambiguatingDescription'], "en_US", "ecommerce")
            disambiguatingDescription['field_value']['fr'] = getValuebyLanguageScope(product["values"]['disambiguatingDescription'], "fr_FR", "ecommerce")
            transformedProduct["fields"].append(disambiguatingDescription)
        # blog_table_description / description
        if "description" in product["values"]:
            description = {}
            description['field_name'] = "blog_table_description"
            description['field_type'] = "multiline_text"
            description['field_value'] = {}
            description['field_value']['de'] = getValuebyLanguageScope(product["values"]['description'], "de_CH", "ecommerce")
            description['field_value']['en'] = getValuebyLanguageScope(product["values"]['description'], "en_US", "ecommerce")
            description['field_value']['fr'] = getValuebyLanguageScope(product["values"]['description'], "fr_FR", "ecommerce")
            transformedProduct["fields"].append(description)
        # blog_seo_latitude / latitude
        if "latitude" in product["values"]:
            latitude = {}
            latitude['field_name'] = "blog_seo_latitude"
            latitude['field_type'] = "1_line_text"
            latitude['readonly'] = 0
            latitude['description'] = None
            latitude['field_value'] = {}
            latitude['field_value']['de'] = product["values"]['latitude'][0]['data']
            latitude['field_value']['en'] = product["values"]['latitude'][0]['data']
            latitude['field_value']['fr'] = product["values"]['latitude'][0]['data']
            transformedProduct["fields"].append(latitude)
        # blog_seo_longitude / longitude
        if "longitude" in product["values"]:
            longitude = {}
            longitude['field_name'] = "blog_seo_longitude"
            longitude['field_type'] = "1_line_text"
            longitude['readonly'] = 0
            longitude['description'] = None
            longitude['field_value'] = {}
            longitude['field_value']['de'] = product["values"]['longitude'][0]['data']
            longitude['field_value']['en'] = product["values"]['longitude'][0]['data']
            longitude['field_value']['fr'] = product["values"]['longitude'][0]['data']
            transformedProduct["fields"].append(longitude)
        # metaserver_address / streetAddress --> critical Field
        if "streetAddress" in product["values"]:
            streetAddress = {}
            streetAddress['field_name'] = "metaserver_address"
            streetAddress['field_type'] = "1_line_text"
            streetAddress['field_value'] = {}
            streetAddress['field_value']['de'] = product["values"]['streetAddress'][0]['data']
            streetAddress['field_value']['en'] = product["values"]['streetAddress'][0]['data']
            streetAddress['field_value']['fr'] = product["values"]['streetAddress'][0]['data']
            transformedProduct["fields"].append(streetAddress)
        # teaser_title_hotel_place / addressLocality
        if "addressLocality" in product["values"]:
            addressLocality = {}
            addressLocality['field_name'] = "teaser_title_hotel_place"
            addressLocality['field_type'] = "1_line_text"
            addressLocality['field_value'] = {}
            addressLocality['field_value']['de'] = product["values"]['addressLocality'][0]['data']
            addressLocality['field_value']['en'] = product["values"]['addressLocality'][0]['data']
            addressLocality['field_value']['fr'] = product["values"]['addressLocality'][0]['data']
            transformedProduct["fields"].append(addressLocality)
            # metaserver_city / addressLocality --> critical Field
            city = {}
            city['field_name'] = "metaserver_city"
            city['field_type'] = "1_line_text"
            city['field_value'] = {}
            city['field_value']['de'] = product["values"]['addressLocality'][0]['data']
            city['field_value']['en'] = product["values"]['addressLocality'][0]['data']
            city['field_value']['fr'] = product["values"]['addressLocality'][0]['data']
            transformedProduct["fields"].append(city)
        # blog_table_contact_details_phone / telephone
        if "telephone" in product["values"]:
            telephone = {}
            telephone['field_name'] = "blog_table_contact_details_phone"
            telephone['field_type'] = "1_line_text"
            telephone['field_value'] = {}
            telephone['field_value']['de'] = getValuebyScope(product["values"]['telephone'], "ecommerce")
            telephone['field_value']['en'] = getValuebyScope(product["values"]['telephone'], "ecommerce")
            telephone['field_value']['fr'] = getValuebyScope(product["values"]['telephone'], "ecommerce")
            transformedProduct["fields"].append(telephone)
        # blog_table_contact_email / email
        if "email" in product["values"]:
            email = {}
            email['field_name'] = "blog_table_contact_email"
            email['field_type'] = "url_link"
            email['field_value'] = {}
            email['field_value']['de'] = getValuebyScope(product["values"]['email'], "ecommerce")
            email['field_value']['en'] = getValuebyScope(product["values"]['email'], "ecommerce")
            email['field_value']['fr'] = getValuebyScope(product["values"]['email'], "ecommerce")
            transformedProduct["fields"].append(email)
        # metaserver_hotel_website / url
        if "url" in product["values"]:
            url = {}
            url['field_name'] = "metaserver_hotel_website"
            url['field_type'] = "url_link"
            url['field_value'] = {}
            url['field_value']['de'] = getValuebyScope(product["values"]['url'], "ecommerce")
            url['field_value']['en'] = getValuebyScope(product["values"]['url'], "ecommerce")
            url['field_value']['fr'] = getValuebyScope(product["values"]['url'], "ecommerce")
            transformedProduct["fields"].append(url)
        # TODO metaserver_trustyou_id / trustyouId

        transformedProducts['records'].append(transformedProduct)
        #print(transformedProduct)
    #print(transformedProducts)
    return transformedProducts

def postImagestoMasch(akeneoProducts):
    for product in akeneoProducts:
        print("Product")
        print(product['identifier'])
        if "maschName" in product["values"]:
            maschName = product["values"]['maschName'][0]['data']
        else:
            print("No MaschName - no Upload")
            continue
        if "image" in product["values"]:
            image = product['values']['image'][0]['data']
            print (image)
        else:
            print("No Image to Upload")
            continue
        sku = product['identifier']
        filepath = "catalog/"+image
        file = getObjectUrl(filepath)

        url = MASCH_URL + "/api/cn/push_record_pictures.php"
        payload = {'user_login': MASCH_USER,
                'user_password': MASCH_PASSWORD,
                'target_record': maschName,
                'target_fields[]': 'teaser_and_content_banner_picture_winter',
                'target_fields[]': 'teaser_and_content_banner_picture_summer'}
        files=[
            ('pictures[]', 
            (sku, requests.get(file).content,'application/octet-stream')
            )]
        headers = {
            'Content-Type': 'multipart/form-data'
        }
        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        print(response.status_code)
        print(response.json())

def postObjecttoMasch(product):
    url = MASCH_URL + MASCH_PUSH_URL
    headers = {'Content-Type': 'application/json'}
    payload = json.dumps(product)
    response = requests.request("PATCH", url, headers=headers, data=payload)
    print(response.status_code)
    #print(response.text)
    #print(json.decoder(r.json()))
    # get response body
    #print(response.json())
    return response

def loadObjectstoMasch(products):
    print("Products")
    #print(products)
    response = postObjecttoMasch(products)
    print("Response")
    print(response.json())
    print("DONE")
    return response

