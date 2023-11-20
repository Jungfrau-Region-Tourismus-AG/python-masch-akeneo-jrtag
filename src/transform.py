from os import getenv
from dotenv import find_dotenv, load_dotenv
import uuid
import validators
import os
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
  print("setValueDict")
  dataValue = []
  for key, value in data.items():
      print(key)
      print(value)
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
  print("setValueList")
  dataValue = []
  for key, value in data.items():
      print(key)
      print(value)

def setValueFloat(data, locale = None, scope = None):
  print("setValueFloat")
  dataValue = []
  value = {}
  value['data'] = data
  value['locale'] = locale
  value['scope'] = scope
  dataValue.append(value)
  return dataValue


def setValue(data, locale = None, scope = None):
  print("setValue")
  if type(data) is str:
    return setValueStr(data, locale, scope)
  elif type(data) is int:
    return setValueInt(data, locale, scope)
  elif type(data) is dict:
    return setValueDict(data, locale, scope)
  elif type(data) is list:
    return setValueList(data, locale, scope)
  elif type(data) is float:
    return setValueStr(data, locale, scope)

def getFieldsValuebyKey(key, data):
  print("getFieldsValuebyKey")
  print(key)
  for field in data['fields']:
    if field["field_name"] == key:
      if not field["field_value"]:
        return ''
      else:
        return field["field_value"]

def checkifValidUrl(url_string):
  print("checkifValidUrl")
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
  print("transformFieldtoAkeneoAttribut")
  field = getFieldsValuebyKey(maschProperty, maschData)
  if field:
      if field['de']:
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
        return getNoneData()
  else:
    return getNoneData()
  
def transformFieldtoAkeneoAttributbyLanguage(maschProperty, maschData, Language, locale, scope, check = None):
  print("transformFieldtoAkeneoAttribut")
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
        return getNoneData()
  else:
    return getNoneData()

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
  print("checkifCategoryinCategories")
  for cat in categories:
    if cat == category:
      return True
  return False

def transform(data, indexAkeneo):
  transformData = []
  dataList = data.copy()
  for item in dataList['records']:
    importProduct = {}
    print(item['record_id'])
    print(item['record_name'])
    if item['record_id'] in indexAkeneo:
      print(indexAkeneo[item['record_id']])
      importProduct['identifier'] = indexAkeneo[item['record_id']]['identifier']
      categoriesArray = indexAkeneo[item['record_id']]['categories']
      if checkIfCategoryInCategories(categoriesArray, AKENEO_CATEGORIES) == False:
        categoriesArray.append(AKENEO_CATEGORIES)
      importProduct['categories'] = categoriesArray
      importProduct['family'] = indexAkeneo[item['record_id']]['family']
      importProduct['enabled'] = True
    else:
      importProduct['identifier'] = str(uuid.uuid4())
      categoriesArray = []
      categoriesArray.append(AKENEO_CATEGORIES)
      importProduct['categories'] = categoriesArray
      importProduct['enabled'] = True
      importProduct['family'] = AKENEO_FAMILY
    
    print(importProduct['categories'])
    # Values
    importProduct['values'] = {}
    importProduct['values']['maschId'] = setValue(item['record_id'])
    importProduct['values']['maschName'] = setValue(item['record_name'])
    importProduct['values']['license'] = setValue('copyrightHolder')
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
    # description
    #importProduct['values']['description'] = transformFieldtoAkeneoAttribut('blog_table_description', item, 'de_CH', 'ecommerce')
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
    stars = getFieldbyLanguage('metaserver_swiss_star', item, 'de')
    print(stars)
    print(type(stars))
    print("starRating_"+str(stars))
    if stars:
      print("starRating_"+stars)
      importProduct['values']['starRating'] = [
        {
          "locale": None,
          "scope": None,
          "data": "starRating_"+str(stars)
        }
      ]

    transformData.append(importProduct)
  return transformData

def transformImage(data, indexAkeneo, maschPropety, attribute, locale = None, scope = None):
  transformData = []
  for item in data['records']:
    if item['record_id'] in indexAkeneo:
      filePath = getFieldsValuebyKey(maschPropety, item)
      print(item['record_id'])
      if filePath:
        if filePath['de']:
          importProduct = {}
          importProduct['identifier'] = indexAkeneo[item['record_id']]['identifier']
          importProduct['filePath'] = filePath['de']
          imagePath = urlparse(filePath['de'])
          filename = os.path.basename(imagePath.path)
          importProduct['filename'] = filename
          importProduct['attribute'] = attribute
          importProduct['locale'] = locale
          importProduct['scope'] = scope
    transformData.append(importProduct)
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
    id = item['values']['maschId'][0]['data']
    transformData[id] = importProduct
  return transformData