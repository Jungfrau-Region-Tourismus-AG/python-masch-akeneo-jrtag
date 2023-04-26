from os import getenv
from dotenv import find_dotenv, load_dotenv
from akeneo.akeneo import Akeneo
import requests
import uuid

load_dotenv(find_dotenv())

AKENEO_HOST = getenv('AKENEO_HOST')
AKENEO_CLIENT_ID = getenv('AKENEO_CLIENT_ID')
AKENEO_CLIENT_SECRET = getenv('AKENEO_CLIENT_SECRET')
AKENEO_USERNAME = getenv('AKENEO_USERNAME')
AKENEO_PASSWORD = getenv('AKENEO_PASSWORD')

MASCH_URL = getenv('MASCH_URL')
MASCH_PULL_URL = getenv('MASCH_PULL_URL')
MASCH_USER = getenv('MASCH_USER')
MASCH_PASSWORD = getenv('MASCH_PASSWORD')


def getMaschPull():
  url = MASCH_URL + MASCH_PULL_URL
  body = {
      "user_login": MASCH_USER,
      "user_password": MASCH_PASSWORD,
      "start_time": "2023-03-01 00:00:00"
  }
  r = requests.get(url, json=body)
  return r.json()

def getAkeneoProducts():
  akeneo = Akeneo(
    AKENEO_HOST,
    AKENEO_CLIENT_ID,
    AKENEO_CLIENT_SECRET,
    AKENEO_USERNAME,
    AKENEO_PASSWORD
  )
  searchQuery = '{"maschId":[{"operator":"NOT EMPTY","value":""}]}'
  return akeneo.getProducts(limit=100, search=searchQuery )

def extract():
  return getMaschPull()

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

def load(data):
  akeneo = Akeneo(
    AKENEO_HOST,
    AKENEO_CLIENT_ID,
    AKENEO_CLIENT_SECRET,
    AKENEO_USERNAME,
    AKENEO_PASSWORD
  )
  for item in data:
    print(item)
    akeneo.patchProductByCode(item['identifier'], item)
    #akeneo.patchProducts(item)

def __main__():
  print("STARTING")
  print("EXTRACTING")
  extractData = extract()
  extractDataAkeneo = getAkeneoProducts()
  
  print("TRANSFORMING")
  transformDataAkeneo = transformAkeneotoMasch(extractDataAkeneo)
  transformData = transform(extractData, transformDataAkeneo)
  
  print(transformDataAkeneo[16042])
  #transformData2 = transfromToAkeneo(transformData)
  print(transformData)
  
  print("LOADING")
  loadData = load(transformData)
  print("DONE")

if __name__== "__main__":
    __main__()