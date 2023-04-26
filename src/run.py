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

def extract():
  return getMaschPull()

def transform(data):
  transformData = []

  for item in data:
    importProduct = {}
    importProduct['identifier'] = uuid.uuid4()
    importProduct['values']['maschId'][0]['data'] = item['record_id']
    importProduct['family'] = "Place"
    importProduct['enabled'] = True
    importProduct['categories'] = ["masch"]
    transformData.append(importProduct)
  return transformData

def load(data):
  akeneo = Akeneo(
    AKENEO_HOST,
    AKENEO_CLIENT_ID,
    AKENEO_CLIENT_SECRET,
    AKENEO_USERNAME,
    AKENEO_PASSWORD
  )
  return akeneo.patchProducts(data)

def __main__():
  print("STARTING")
  print("EXTRACTING")
  extractData = extract()
  print("TRANSFORMING")
  transformData = transform(extractData)
  print("LOADING")
  loadData = load(transformData)
  print(loadData)
  print("DONE")

if __name__== "__main__":
    __main__()