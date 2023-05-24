import uuid
import validators

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
      print(key)
      print(value)
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
      print(key)
      print(value)
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
      print(key)
      print(value)
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
  for field in data['fields']:
    if field["field_name"] == key:
      print(field["field_name"])
      print (type(field["field_value"]))
      print (field["field_value"])
      if not field["field_value"]:
        return ''
      else:
        print (type(field["field_value"]))
        print (field["field_name"])
        return field["field_value"]

def checkifValidUrl(url_string):
  print("checkifValidUrl")
  result = validators.url(url_string)
  print(result)
  return result

def transformFieldtoAkeneoAttribut(maschProperty, maschData, local, scope, check = None):
  print("transformFieldtoAkeneoAttribut")
  field = getFieldsValuebyKey(maschProperty, maschData)
  print (field)
  if field:
      print(field['de'])
      if check == 'url':
        result = validators.url(field['de'])
        print (result)
      fieldValue = setValue(field['de'], local, scope)
      print(fieldValue)
      return fieldValue
  else:
    print ("No field")

def transform(data, indexAkeneo):
  transformData = []
  for item in data['records']:
    importProduct = {}
    if item['record_id'] in indexAkeneo:
      importProduct['identifier'] = indexAkeneo[item['record_id']]['identifier']
    else:
      importProduct['identifier'] = str(uuid.uuid4())
    print(item['record_id'])
    importProduct['family'] = "Place"
    importProduct['enabled'] = True
    importProduct['categories'] = ["masch"]

    # Values
    importProduct['values'] = {}
    dataValue = setValue(item['record_id'])
    importProduct['values']['maschId'] = dataValue
    # name
    importProduct['values']['name'] = transformFieldtoAkeneoAttribut('teaser_title_hotel_name', item, 'de_CH', None)
    # description
    importProduct['values']['description'] = transformFieldtoAkeneoAttribut('blog_table_description', item, 'de_CH', 'ecommerce')
    # url
    # Locale : None, spezifisch/default (bspw. de_CH) or All
    # Scope : None, spezifisch/default (bspw. ecommerce) or All
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
    importProduct['values']['addressLocality'] = transformFieldtoAkeneoAttribut('teaser_title_hotel_place', item, None, None)
    # streetAddress / metaserver_address
    importProduct['values']['streetAddress'] = transformFieldtoAkeneoAttribut('metaserver_address', item, None, None)
    # addressCountry / metaserver_country
    importProduct['values']['addressCountry'] = transformFieldtoAkeneoAttribut('metaserver_country', item, None, None)
    # Geo
    # latitude / blog_seo_latitude
    importProduct['values']['latitude'] = transformFieldtoAkeneoAttribut('blog_seo_latitude', item, None, None)
    # longitude / blog_seo_longitude
    importProduct['values']['longitude'] = transformFieldtoAkeneoAttribut('blog_seo_longitude', item, None, None)
    # blog_table_video_url_link
    # teaser_video_id

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
    print(item['identifier'])
    print(item['values']['maschId'][0]['data'])
    id = item['values']['maschId'][0]['data']
    transformData[id] = importProduct
  return transformData