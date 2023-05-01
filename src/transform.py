import uuid

def setValue(data, locale = None, scope = None):
  if type(data) is str:
    dataValue = []
    value = {}
    value['data'] = data
    value['locale'] = locale
    value['scope'] = scope
    dataValue.append(value)
    return dataValue
  elif type(data) is int:
    dataValue = []
    value = {}
    value['data'] = data
    value['locale'] = locale
    value['scope'] = scope
    dataValue.append(value)
    return dataValue
  elif type(data) is dict:
    dataValue = []
    for key, value in data.items():
      print(key)
      print(value)
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
    return dataValue
  
def setValueDict(data, locale = None, scope = None):
  dataValue = []
  for key, value in data.items():
      print(key)
      print(value)
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
  return dataValue

def getFieldsValuebyKey(key, data):
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
    importProduct['values']['maschId'] = []
    dataValue = setValue(item['record_id'])
    importProduct['values']['maschId'] = dataValue
    # name
    importProduct['values']['name'] = []
    name = getFieldsValuebyKey('teaser_title_hotel_name', item)
    nameValue = setValue(name, 'de_CH')
    importProduct['values']['name'] = nameValue
    # description
    importProduct['values']['description'] = []
    description = getFieldsValuebyKey('blog_table_description', item)
    descriptionValue = setValue(description, 'de_CH', 'ecommerce')
    importProduct['values']['description'] = descriptionValue
    # url
    importProduct['values']['url'] = []
    url = getFieldsValuebyKey('metaserver_hotel_website', item)
    urlValue = setValue(url, 'de_CH', 'ecommerce')
    importProduct['values']['url'] = urlValue
    # email
    importProduct['values']['email'] = []
    email = getFieldsValuebyKey('blog_table_contact_email', item)
    emailValue = setValue(email, 'de_CH', 'ecommerce')
    importProduct['values']['email'] = emailValue
    # telephone
    importProduct['values']['telephone'] = []
    telephone = getFieldsValuebyKey('blog_table_contact_phone', item)
    telephoneValue = setValue(telephone, 'de_CH', 'ecommerce')
    importProduct['values']['telephone'] = telephoneValue
    # addressLocality
    importProduct['values']['addressLocality'] = []
    addressLocality = getFieldsValuebyKey('blog_table_address_locality', item)
    addressLocalityValue = setValue(addressLocality, 'de_CH', 'ecommerce')
    importProduct['values']['addressLocality'] = addressLocalityValue

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