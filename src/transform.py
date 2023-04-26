import uuid

def setValue(data, locale = None, scope = None):
    dataValue = {}
    dataValue['data'] = data
    dataValue['locale'] = locale
    dataValue['scope'] = scope
    return dataValue

def getFieldsValuebyKey(key, data):
  for field in data['fields']:
    if field["field_name"] == "teaser_title_hotel_name":
      return field["field_value"]['de']

def transform(data, indexAkeneo):
  transformData = []
  for item in data['records']:
    importProduct = {}
    if item['record_id'] in indexAkeneo:
      importProduct['identifier'] = indexAkeneo[item['record_id']]['identifier']
    else:
      importProduct['identifier'] = str(uuid.uuid4())
    print(item['record_id'])
    importProduct['values'] = {}
    importProduct['values']['maschId'] = []
    dataValue = setValue(item['record_id'])
    importProduct['values']['maschId'].append(dataValue)
    importProduct['values']['name'] = []
    name = getFieldsValuebyKey('teaser_title_hotel_name', item)
    nameValue = setValue(name, 'de_CH')
    importProduct['values']['name'].append(nameValue)
    importProduct['family'] = "Place"
    importProduct['enabled'] = True
    importProduct['categories'] = ["masch"]
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