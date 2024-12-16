from os import getenv
from dotenv import find_dotenv, load_dotenv
import uuid
import validators
import datetime
import os
import features as featuresChecklist
from urllib.parse import urlparse
load_dotenv(find_dotenv())

AKENEO_CATEGORIES = getenv('AKENEO_CATEGORIES')
AKENEO_FAMILY = getenv('AKENEO_FAMILY')

def setValue(data):
  dataValue = []
  value = {}
  value['data'] = data
  value['locale'] = None
  value['scope'] = None
  return data

def setValueLocale(data):
  dataValue = []
  for key, value in data.items():
      if key == 'de':
        deValue = {}
        deValue['data'] = value
        deValue['locale'] = 'de_CH'
        deValue['scope'] = None
        dataValue.append(deValue)
      elif key == 'en':
        enValue = {}
        enValue['data'] = value
        enValue['locale'] = 'en_US'
        enValue['scope'] = None
        dataValue.append(enValue)
      elif key == 'fr':
        frValue = {}
        frValue['data'] = value
        frValue['locale'] = 'fr_FR'
        frValue['scope'] = None
        dataValue.append(frValue)
  return dataValue

def setValueScope(data, locale = None, scope = None):
  dataValue = []
  for key, value in data.items():
      if key == 'de':
        deValue = {}
        deValue['data'] = value
        deValue['locale'] = locale
        deValue['scope'] = scope
        dataValue.append(deValue)
      elif key == 'en':
        enValue = {}
        enValue['data'] = value
        enValue['locale'] = locale
        enValue['scope'] = scope
        dataValue.append(enValue)
      elif key == 'fr':
        frValue = {}
        frValue['data'] = value
        frValue['locale'] = locale
        frValue['scope'] = scope
        dataValue.append(frValue)
  return dataValue

def setValue(data, locale, scope):
  dataValue = []
  for key, value in data.items():
      if key == 'de':
        deValue = {}
        deValue['data'] = value
        deValue['locale'] = None
        deValue['scope'] = 'ecommerce'
        dataValue.append(deValue)
      elif key == 'en':
        enValue = {}
        enValue['data'] = value
        enValue['locale'] = None
        enValue['scope'] = 'ecommerce'
        dataValue.append(enValue)
      elif key == 'fr':
        frValue = {}
        frValue['data'] = value
        frValue['locale'] = None
        frValue['scope'] = 'ecommerce'
        dataValue.append(frValue)
  return dataValue

def setValueStr(data, locale, scope):
  dataValue = []
  value = {}
  value['data'] = str(data)
  value['locale'] = locale
  value['scope'] = scope
  dataValue.append(value)
  return dataValue

def setValueInt(data, locale, scope):
  dataValue = []
  value = {}
  value['data'] = data
  value['locale'] = locale
  value['scope'] = scope
  dataValue.append(value)
  return dataValue

def setValueDict(data, locale = None, scope = None):
  #print("setValueDict")
  dataValue = []
  for key, value in data.items():
      #print(key)
      #print(value)
      if locale is not None:
        if key == 'de':
          deValue = {}
          deValue['data'] = value
          deValue['locale'] = 'de_CH'
          deValue['scope'] = scope
          dataValue.append(deValue)
        elif key == 'en':
          enValue = {}
          enValue['data'] = value
          enValue['locale'] = 'en_US'
          enValue['scope'] = scope
          dataValue.append(enValue)
        elif key == 'fr':
          frValue = {}
          frValue['data'] = value
          frValue['locale'] = 'fr_FR'
          frValue['scope'] = scope
          dataValue.append(frValue)
      else:
        if key == 'de':
          newValue = {}
          newValue['data'] = value
          newValue['locale'] = locale
          newValue['scope'] = scope
          dataValue.append(newValue)
  return dataValue

def setValueList(data, locale = None, scope = None):
  #print("setValueList")
  dataValue = []
  for key, value in data.items():
      print("Check setValueList")
      #print(key + " - " + value)
      #print(key)
      #print(value)

def setValueFloat(data, locale = None, scope = None):
  #print("setValueFloat")
  dataValue = []
  value = {}
  value['data'] = data
  value['locale'] = locale
  value['scope'] = scope
  dataValue.append(value)
  return dataValue


def setValue(data, locale = None, scope = None):
  #print("setValue")
  if type(data) is str:
    return setValueStr(data, locale, scope)
  elif type(data) is int:
    return setValueInt(data, locale, scope)
  elif type(data) is dict:
    return setValueDict(data, locale, scope)
  elif type(data) is list:
    print('setValueList')
    return setValueList(data, locale, scope)
  elif type(data) is float:
    return setValueStr(data, locale, scope)

def getFieldsValuebyKey(key, data):
  #print("getFieldsValuebyKey")
  #print(key)
  for field in data['fields']:
    if field["field_name"] == key:
      if not field["system_field_value"]:
        return ''
      else:
        return field["system_field_value"]

def checkifValidUrl(url_string):
  #print("checkifValidUrl")
  result = validators.url(url_string)
  return result

def getNoneData():
  dataValue = []
  value = {}
  value['data'] = None
  value['locale'] = None
  value['scope'] = None
  dataValue.append(value)
  return dataValue

def transformFieldtoAkeneoAttribut(maschProperty, maschData, local, scope, check = None):
  #print("transformFieldtoAkeneoAttribut")
  field = getFieldsValuebyKey(maschProperty, maschData)
  if field:
      #print(field)
      #print(type(field))
      if type(field) is str:
        return setValue(field, local, scope)
      elif type(field) is int:
        return setValue(field, local, scope)
      elif field['de']:
        if check == 'url':
          result = validators.url(field['de'])
          if result == True:
            fieldValue = setValue(field['de'], local, scope)
          else:
            newURL = 'https://' + field['de']
            fieldValue = setValue(newURL, local, scope)
        else:
          fieldValue = setValue(field['de'], local, scope)
        return fieldValue
      else:
        return setValue(field, local, scope)
        #return getNoneData()
  else:
    #return setValue(field, local, scope)
    return getNoneData()
  
def transformFieldtoAkeneoAttributbyLanguage(maschProperty, maschData, Language, locale, scope, check = None):
  #print("transformFieldtoAkeneoAttribut")
  field = getFieldsValuebyKey(maschProperty, maschData)
  if field:
      if field[Language]:
        if check == 'url':
          result = validators.url(field[Language])
          if result == True:
            fieldValue = setValue(field[Language], locale, scope)
          else:
            newURL = 'https://' + field[Language]
            fieldValue = setValue(newURL, locale, scope)
        else:
          fieldValue = setValue(field[Language], locale, scope)
        return fieldValue
      else:
        return getNoneData()
  else:
    return getNoneData()
  
def getFieldbyLanguage(maschProperty, maschData, Language, check = None):
  field = getFieldsValuebyKey(maschProperty, maschData)
  if field:
      if field[Language]:
        if check == 'url':
          result = validators.url(field[Language])
          if result == True:
            fieldValue = field[Language]
          else:
            newURL = 'https://' + field[Language]
            fieldValue = newURL
        else:
          fieldValue = field[Language]
        return fieldValue
      else:
        return None
  else:
    return None

def setValuebyLocaleScope(data, locale, scope):
  dataValue = []
  for row in data:
    value = {}
    value['data'] = row
    value['locale'] = locale
    value['scope'] = scope
    dataValue.append(value)

  return dataValue

def transformFieldtoAkeneoAttributebyLocale(maschProperty, maschData, locale, scope):
  field = getFieldsValuebyKey(maschProperty, maschData)
  if field:
      fieldValue = [
        {
          "locale": 'de_CH',
          "scope": scope,
          "data": field['de']
        },
        {
          "locale": locale,
        }
      ]
      if field['de']:
        fieldValue = setValue(field['de'], locale, scope)
        return fieldValue
      else:
        return getNoneData()
  else:
    return getNoneData()

def checkIfCategoryInCategories(categories, category):
  #print("checkifCategoryinCategories")
  for cat in categories:
    if cat == category:
      return True
  return False

def getItembyMaschId(data, maschId):
  if maschId in data:
    return data[maschId]
  else:
    return None

def transform(data, indexAkeneo):
  transformData = []
  dataList = data.copy()
  hashMasch = createHashMASCH(indexAkeneo)
  for item in dataList['records']:
    importProduct = {}
    if item['record_id'] == None:
      continue
    print("    - CHECK: "+str(item['record_id'])+" - "+item['record_name'])
    #if item['record_id'] in indexAkeneo:
    if str(item['record_id']) in hashMasch:
      print("     - Record ID in Akeneo")
      #print(indexAkeneo[item['record_id']])
      akeneoProduct = [product for product in indexAkeneo if product['values']['maschId'][0]['data'] == str(item['record_id'])]
      print("     - Identifier: "+akeneoProduct[0]['identifier'])
      importProduct['identifier'] = akeneoProduct[0]['identifier']
      categoriesArray = akeneoProduct[0]['categories']
      if checkIfCategoryInCategories(categoriesArray, AKENEO_CATEGORIES) == False:
        categoriesArray.append(AKENEO_CATEGORIES)
      importProduct['categories'] = categoriesArray
      importProduct['family'] = akeneoProduct[0]['family']
      #importProduct['enabled'] = True
    else:
      print("      - Record ID not in Akeneo")
      importProduct['identifier'] = str(uuid.uuid4())
      categoriesArray = []
      categoriesArray.append(AKENEO_CATEGORIES)
      importProduct['categories'] = categoriesArray
      #importProduct['enabled'] = True
      importProduct['family'] = AKENEO_FAMILY
    
    #print(importProduct['categories'])
    # Values
    importProduct['values'] = {}
    importProduct['values']['maschId'] = setValue(str(item['record_id']))
    importProduct['values']['maschName'] = setValue(item['record_name'])
    # maschUpdated
    nowDatetime = datetime.datetime.now()
    valueMaschUpdeted = str(nowDatetime.strftime("%Y-%m-%dT%H:%M:%S"))
    #print(valueMaschUpdeted)
    importProduct['values']['maschUpdated'] = [{
      "data": valueMaschUpdeted,
      "locale": None,
      "scope": None
    }]
    
    importProduct['values']['license'] = setValue('copyright')
    importProduct['values']['copyrightHolder'] = setValue('MASCH')
    # name
    #importProduct['values']['name'] = transformFieldtoAkeneoAttribut('teaser_title_hotel_name', item, 'de_CH', None)
    importProduct['values']['name'] = [
      {
        "locale": "de_CH",
        "scope": None,
        "data": getFieldbyLanguage('teaser_title_hotel_name', item, 'de')
      },
      {
        "locale": "en_US",
        "scope": None,
        "data": getFieldbyLanguage('teaser_title_hotel_name', item, 'en')
      },
      {
        "locale": "fr_FR",
        "scope": None,
        "data": getFieldbyLanguage('teaser_title_hotel_name', item, 'fr')
      }
    ]
    ## Mehrsprachigkeit
    #disambiguatingDescription
    importProduct['values']['disambiguatingDescription'] = [
      {
        "locale": "de_CH",
        "scope": "ecommerce",
        "data": getFieldbyLanguage('teaser_text_desktop', item, 'de')
      },
      {
        "locale": "en_US",
        "scope": "ecommerce",
        "data": getFieldbyLanguage('teaser_text_desktop', item, 'en')
      },
      {
        "locale": "fr_FR",
        "scope": "ecommerce",
        "data": getFieldbyLanguage('teaser_text_desktop', item, 'fr')
      }
    ]
    # description
    importProduct['values']['description'] = [
      {
        "locale": "de_CH",
        "scope": "ecommerce",
        "data": getFieldbyLanguage('blog_table_description', item, 'de')
      },
      {
        "locale": "en_US",
        "scope": "ecommerce",
        "data": getFieldbyLanguage('blog_table_description', item, 'en')
      },
      {
        "locale": "fr_FR",
        "scope": "ecommerce",
        "data": getFieldbyLanguage('blog_table_description', item, 'fr')
      }
    ]
    # url
    importProduct['values']['url'] = transformFieldtoAkeneoAttribut('metaserver_hotel_website', item, None, 'ecommerce', 'url')
    # email
    importProduct['values']['email'] = transformFieldtoAkeneoAttribut('blog_table_contact_email', item, None, 'ecommerce')
    # telephone
    # Not in MASCH
    #importProduct['values']['telephone'] = []
    #telephone = getFieldsValuebyKey('blog_table_contact_phone', item)
    #telephoneValue = setValue(telephone['de'], None, 'ecommerce')
    #importProduct['values']['telephone'] = telephoneValue
    # addressLocality / teaser_title_hotel_place - Alternative: metaserver_city
    #importProduct['values']['addressLocality'] = transformFieldtoAkeneoAttribut('teaser_title_hotel_place', item, None, None)
    # streetAddress / metaserver_address
    #importProduct['values']['streetAddress'] = transformFieldtoAkeneoAttribut('metaserver_address', item, None, None)
    # addressCountry / metaserver_country
    #importProduct['values']['addressCountry'] = transformFieldtoAkeneoAttribut('metaserver_country', item, None, None)
    
    # Geo
    # latitude / blog_seo_latitude
    importProduct['values']['latitude'] = transformFieldtoAkeneoAttribut('blog_seo_latitude', item, None, None)
    # longitude / blog_seo_longitude
    importProduct['values']['longitude'] = transformFieldtoAkeneoAttribut('blog_seo_longitude', item, None, None)
    # blog_table_video_url_link
    # teaser_video_id

    # Call-To-Action
    #importProduct['values']['action_button_url'] = transformFieldtoAkeneoAttribut('teaser_booking_button_url_mobil', item, None, None)
    importProduct['values']['action_button_url'] = [
      {
        "locale": "de_CH",
        "scope": "ecommerce",
        "data": getFieldbyLanguage('teaser_booking_button_url_mobil', item, 'de', 'url')
      },
      {
        "locale": "en_US",
        "scope": "ecommerce",
        "data": getFieldbyLanguage('teaser_booking_button_url_mobil', item, 'en', 'url')
      },
      {
        "locale": "fr_FR",
        "scope": "ecommerce",
        "data": getFieldbyLanguage('teaser_booking_button_url_mobil', item, 'fr', 'url')
      }
    ]
    importProduct['values']['action_button_text'] = [
      {
        "locale": "de_CH",
        "scope": "ecommerce",
        "data": "booking"
      },
      {
        "locale": "en_US",
        "scope": "ecommerce",
        "data": "booking"
      },
      {
        "locale": "fr_FR",
        "scope": "ecommerce",
        "data": "booking"
      }
    ]
    #stars = getFieldbyLanguage('metaserver_swiss_star', item, 'de')
    stars = getFieldsValuebyKey('metaserver_swiss_star', item)
    if stars:
      if type(stars) is int:
        if stars <=5 and stars >= 1:
          importProduct['values']['starRating'] = [
            {
              "locale": None,
              "scope": None,
              "data": "starRating_"+str(stars)
            }
          ]

    # Ausstattungen
    # metaserver_hotel_features <-> features
    #importProduct['values']['features'] = transformFieldtoAkeneoAttribut('metaserver_hotel_features', item, None, None)
    #print("Features DEBUG")
    #features = getFieldbyLanguage('metaserver_hotel_features', item, 'de')
    features = getFieldsValuebyKey('metaserver_hotel_features', item)
    #print("Set features Variable")
    #print(features)

    if features:
      print("features is not None")
      newFeatures = checkFeatures(features, featuresChecklist.features)
      print(type(newFeatures))
      importProduct['values']['features'] = [{
        "locale": None,
        "scope": None,
        "data": newFeatures
      }]

    transformData.append(importProduct)
  return transformData

def transformImage(data, indexAkeneo, maschPropety, attribute, locale = None, scope = None):
  transformData = []
  hashMasch = createHashMASCH(indexAkeneo)
  for item in data['records']:
    print(" - CHECK: "+str(item['record_id'])+" - "+item['record_name'])
    if str(item['record_id']) in hashMasch:
      print("  - Record ID in Akeneo")
      akeneoProduct = [product for product in indexAkeneo if product['values']['maschId'][0]['data'] == str(item['record_id'])]
      filePath = getFieldsValuebyKey(maschPropety, item)
      print("record_id: "+str(item['record_id']))
      if filePath:
        print("in FilePath")
        if filePath['de']:
          print("in de")
          productImage = {}
          productImage['identifier'] = akeneoProduct[0]['identifier']
          productImage['filePath'] = filePath['de']
          imagePath = urlparse(filePath['de'])
          filename = os.path.basename(imagePath.path)
          productImage['filename'] = filename
          productImage['attribute'] = attribute
          productImage['locale'] = locale
          productImage['scope'] = scope
          print("Variabe productImage")
          print(productImage)
    transformData.append(productImage)
  return transformData

def transfromToAkeneo(data):
  dataString = ''
  for item in data:
    dataString += str(item)
    dataString += '\r\n'
  return dataString

def transformAkeneotoMasch(data):
  transformData = {}
  for item in data:
    importProduct = {}
    importProduct['identifier'] = item['identifier']
    importProduct['categories'] = item['categories']
    importProduct['family'] = item['family']
    importProduct['enabled'] = item['enabled']
    print(item['identifier'])
    print(item['values']['maschId'][0]['data'])
    id = str(item['values']['maschId'][0]['data'])
    transformData[id] = importProduct
  return transformData

def checkFeatures(data, checklist):
  result = []    
  for value in data:
    print(value)
    if value in checklist:
      result.append(checklist[value])

  print(result)
  return result

def createHashAkeneo(data):
  hashData = {}
  for item in data:
    hashData[item['identifier']] = item
  return hashData

def createHashMASCH(data):
  idSet = {item['values']['maschId'][0]['data'] for item in data}
  return idSet