import uuid

def setValue(data):
    dataValue = {}
    dataValue['data'] = data
    dataValue['locale'] = None
    dataValue['scope'] = None
    return dataValue

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